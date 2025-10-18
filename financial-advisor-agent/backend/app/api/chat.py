"""
Chat API endpoints with streaming support via Server-Sent Events (SSE).
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Generator
import json
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message as MessageModel
from app.api.dependencies import get_current_user
from app.agents.main_agent import create_financial_advisor_agent
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    conversation_id: Optional[str] = None
    stream: bool = True


class ChatResponse(BaseModel):
    """Response model for non-streaming chat."""

    response: str
    conversation_id: str
    message_id: str
    tool_calls: Optional[list] = None
    sources: Optional[list] = None


def get_or_create_conversation(
    db: Session, user: Optional[User], conversation_id: Optional[str] = None
) -> Conversation:
    """Get existing conversation or create a new one."""

    # For testing without auth, use first user or create one
    if not user:
        user = db.query(User).first()

        if not user:
            # Create a test user if none exists
            user = User(
                email="test@example.com",
                full_name="Test User",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

    if conversation_id:
        # Try to get existing conversation
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation and conversation.user_id == user.id:
            return conversation

    # Create new conversation
    conversation = Conversation(
        user_id=user.id,
        title=f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def save_message(
    db: Session, conversation: Conversation, role: str, content: str
) -> MessageModel:
    """Save a message to the database."""

    message = MessageModel(
        conversation_id=conversation.id,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def stream_agent_response(
    user_message: str, user: User, conversation_id: str, db: Session
) -> Generator[str, None, None]:
    """
    Stream agent responses using Server-Sent Events (SSE).

    Yields SSE-formatted chunks of the agent's response.
    """

    try:
        # Get conversation
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation or conversation.user_id != user.id:
            yield f"event: error\ndata: {json.dumps({'error': 'Conversation not found'})}\n\n"
            return

        # Save user message
        user_msg = save_message(db, conversation, "user", user_message)

        # Send user message confirmation
        yield f"event: message\ndata: {json.dumps({'type': 'user', 'content': user_message, 'id': str(user_msg.id)})}\n\n"

        # Create agent with user context
        agent_executor = create_financial_advisor_agent(
            model_name="claude-sonnet-4-20250514",
            thread_id=conversation_id
        )

        # Prepare agent input
        config = {
            "configurable": {
                "thread_id": conversation_id,
                "user_id": str(user.id),
            }
        }

        # Send typing indicator
        yield f"event: typing\ndata: {json.dumps({'typing': True})}\n\n"

        # Collect full response for saving
        full_response = ""
        tool_calls_list = []

        # Stream agent response
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
        ):
            # Handle different types of chunks
            if "agent" in chunk:
                # Agent is thinking/responding
                agent_message = chunk["agent"]["messages"][0]

                if hasattr(agent_message, "content") and agent_message.content:
                    content = agent_message.content
                    full_response += content

                    # Send content chunk
                    yield f"event: chunk\ndata: {json.dumps({'content': content})}\n\n"

                # Track tool calls
                if hasattr(agent_message, "tool_calls") and agent_message.tool_calls:
                    for tool_call in agent_message.tool_calls:
                        tool_info = {
                            "name": tool_call.get("name", "unknown"),
                            "arguments": tool_call.get("args", {}),
                        }
                        tool_calls_list.append(tool_info)

                        # Send tool call notification
                        yield f"event: tool\ndata: {json.dumps(tool_info)}\n\n"

            elif "tools" in chunk:
                # Tool execution result
                tool_messages = chunk["tools"]["messages"]
                for tool_msg in tool_messages:
                    if hasattr(tool_msg, "name") and hasattr(tool_msg, "content"):
                        # Update tool call with result
                        for tool_call in tool_calls_list:
                            if tool_call["name"] == tool_msg.name:
                                tool_call["result"] = str(tool_msg.content)[:200]  # Truncate long results

                        # Send tool result notification
                        yield f"event: tool_result\ndata: {json.dumps({'tool': tool_msg.name, 'result': 'completed'})}\n\n"

        # Save assistant message
        assistant_msg = save_message(db, conversation, "assistant", full_response)

        # Update message metadata with tool calls
        if tool_calls_list:
            assistant_msg.message_metadata = {"tool_calls": tool_calls_list}
            db.commit()

        # Send completion event
        yield f"event: done\ndata: {json.dumps({'id': str(assistant_msg.id), 'tool_calls': tool_calls_list})}\n\n"

    except Exception as e:
        # Send error event
        error_message = f"An error occurred: {str(e)}"
        yield f"event: error\ndata: {json.dumps({'error': error_message})}\n\n"


@router.post("/stream")
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Stream chat responses using Server-Sent Events (SSE).

    The response is a stream of events:
    - `message`: Echoes the user message
    - `typing`: Agent is processing
    - `chunk`: Partial response content
    - `tool`: Tool call notification
    - `tool_result`: Tool execution completed
    - `done`: Response complete with metadata
    - `error`: Error occurred
    """

    # Get or create conversation (user is None for testing)
    conversation = get_or_create_conversation(db, None, request.conversation_id)

    # Get the user from conversation
    user = db.query(User).filter(User.id == conversation.user_id).first()

    # Return streaming response
    return StreamingResponse(
        stream_agent_response(request.message, user, str(conversation.id), db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering in nginx
        },
    )


@router.post("/message", response_model=ChatResponse)
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Send a chat message and get a complete response (non-streaming).

    This endpoint waits for the full response before returning.
    Use the /stream endpoint for real-time streaming.
    """

    # Get or create conversation
    conversation = get_or_create_conversation(db, None, request.conversation_id)

    # Get user from conversation
    user = db.query(User).filter(User.id == conversation.user_id).first()

    try:
        # Save user message
        user_msg = save_message(db, conversation, "user", request.message)

        # Create agent with user context
        agent_executor = create_financial_advisor_agent(
            model_name="claude-sonnet-4-20250514",
            thread_id=str(conversation.id)
        )

        # Prepare agent input
        config = {
            "configurable": {
                "thread_id": str(conversation.id),
                "user_id": str(user.id),
            }
        }

        # Get agent response
        response = agent_executor.invoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
        )

        # Extract response content
        agent_messages = response.get("messages", [])
        assistant_message = None

        for msg in reversed(agent_messages):
            if isinstance(msg, AIMessage):
                assistant_message = msg
                break

        if not assistant_message:
            raise HTTPException(status_code=500, detail="No response from agent")

        # Extract tool calls if any
        tool_calls = []
        if hasattr(assistant_message, "tool_calls") and assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_calls.append({
                    "name": tool_call.get("name", "unknown"),
                    "arguments": tool_call.get("args", {}),
                })

        # Save assistant message
        assistant_msg = save_message(
            db, conversation, "assistant", assistant_message.content
        )

        # Update metadata
        if tool_calls:
            assistant_msg.message_metadata = {"tool_calls": tool_calls}
            db.commit()

        return ChatResponse(
            response=assistant_message.content,
            conversation_id=str(conversation.id),
            message_id=str(assistant_msg.id),
            tool_calls=tool_calls,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
def list_conversations(
    db: Session = Depends(get_db),
):
    """List all conversations for the current user."""

    # Get first user (for testing without auth)
    user = db.query(User).first()
    if not user:
        return []

    conversations = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).order_by(Conversation.updated_at.desc()).all()

    return [
        {
            "id": str(conv.id),
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
        }
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    """Get all messages in a conversation."""

    # Get first user (for testing without auth)
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify conversation ownership
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get messages
    messages = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.created_at.asc()).all()

    return [
        {
            "id": str(msg.id),
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
            "metadata": msg.message_metadata,
        }
        for msg in messages
    ]


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    """Delete a conversation and all its messages."""

    # Get first user (for testing without auth)
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify conversation ownership
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation or conversation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Delete conversation (cascade will delete messages)
    db.delete(conversation)
    db.commit()

    return {"status": "deleted", "conversation_id": conversation_id}
