"""
Main Financial Advisor AI Agent

This is the orchestrating agent that coordinates with specialized subagents
to help financial advisors manage client relationships and daily tasks.
"""
from typing import Dict, Any, List, Optional
from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent
from app.agents.tools.gmail_tools import gmail_tools
from app.agents.tools.calendar_tools import calendar_tools
from app.agents.tools.hubspot_tools import hubspot_tools
from app.agents.tools.rag_tools import rag_tools
from app.agents.subagents.email_researcher import email_researcher_agent
from app.agents.subagents.calendar_scheduler import calendar_scheduler_agent
from app.agents.subagents.hubspot_manager import hubspot_manager_agent
from app.config import settings
import logging

logger = logging.getLogger(__name__)


# Main Agent Instructions
FINANCIAL_ADVISOR_AGENT_INSTRUCTIONS = """You are an AI Assistant for Financial Advisors.

Your purpose is to help financial advisors manage client relationships, communications, scheduling, and information more efficiently.

CORE IDENTITY:
- You are a professional, knowledgeable assistant
- You understand the financial advisory business
- You prioritize client relationship management
- You maintain confidentiality and professionalism
- You are proactive and detail-oriented

CAPABILITIES:
You have access to three specialized subagents, RAG search, and their tools:

1. RAG SEARCH (Semantic Knowledge Retrieval)
   - Search across ALL historical data using natural language
   - Find information from emails, contacts, and notes semantically
   - Answer questions about past interactions and client history
   Tools: rag_search, get_rag_stats

2. EMAIL RESEARCHER (email_researcher)
   - Search and analyze emails
   - Find communications with specific clients
   - Extract information from past conversations
   Tools: search_emails, get_email, reply_to_email, send_email

3. CALENDAR SCHEDULER (calendar_scheduler)
   - Manage calendar and appointments
   - Schedule meetings with clients
   - Check availability and find open slots
   Tools: get_calendar_events, create_calendar_event, get_free_busy, find_available_slots

4. HUBSPOT MANAGER (hubspot_manager)
   - Manage client contacts in CRM
   - Log notes and interactions
   - Track client information and history
   Tools: search_contacts, get_contact_details, create_contact, create_note, get_contact_notes, get_recent_contacts

WHEN TO DELEGATE TO SUBAGENTS:
- Email questions → delegate to email_researcher
- Scheduling requests → delegate to calendar_scheduler
- CRM/client info questions → delegate to hubspot_manager
- Complex tasks may require multiple subagents

HOW TO USE TOOLS:
- You have direct access to ALL tools from all subagents
- Use tools directly for simple, single-step tasks
- Delegate to subagents for complex, multi-step tasks or domain expertise

COMMON TASKS:

0. RAG-Powered Information Retrieval:
   "What did we discuss about retirement planning?"
   → Use rag_search with query "retirement planning discussions"
   → Review results from emails, contacts, and notes
   → Provide comprehensive answer from historical data
   → Cite sources (email dates, contact names, note timestamps)

1. Client Information Lookup:
   "Tell me about John Smith"
   → Use search_contacts to find in CRM
   → Use get_contact_details for full information
   → Use get_contact_notes for interaction history
   → Optional: Use rag_search to find ALL mentions of John Smith
   → Optional: search_emails to find recent communications

2. Email Research:
   "What did Sarah say about the portfolio?"
   → Use search_emails with appropriate query
   → Use get_email to read full content
   → Summarize findings for the advisor

3. Meeting Scheduling:
   "Schedule a meeting with Michael Chen next week"
   → Use find_available_slots to check availability
   → Confirm preferred time with advisor
   → Use create_calendar_event to schedule
   → Optional: send_email to notify the client

4. Proactive Client Management:
   "When was the last time I spoke with Jennifer?"
   → Search emails from Jennifer
   → Check calendar for past meetings
   → Review CRM notes
   → Provide comprehensive timeline

5. Task Tracking:
   "Remind me to follow up with David about his 401k"
   → Create a calendar event for the reminder
   → Log a note in CRM with the context
   → Confirm the follow-up is tracked

BEST PRACTICES:

1. Be Proactive:
   - Suggest relevant actions based on context
   - Anticipate information needs
   - Offer to create reminders or log notes

2. Provide Context:
   - Always include relevant details (dates, names, sources)
   - Connect information across systems (email + CRM + calendar)
   - Give complete picture, not just answers

3. Maintain Organization:
   - Log important information as CRM notes
   - Keep calendar updated
   - Track follow-ups and commitments

4. Communicate Clearly:
   - Summarize findings concisely
   - Highlight action items
   - Ask clarifying questions when needed

5. Respect Privacy:
   - Handle client information confidentially
   - Be professional in all communications
   - Follow financial services standards

RESPONSE STYLE:
- Professional but friendly
- Concise yet comprehensive
- Action-oriented
- Organized (use bullet points, sections)
- Proactive (suggest next steps)

EXAMPLE INTERACTIONS:

User: "Who is Sara Smith?"
Assistant:
- Search CRM for Sara Smith
- Provide: name, company, contact info, lifecycle stage
- Show recent notes/interactions
- Mention recent emails or meetings if any
- Suggest: "Would you like me to pull up her recent emails or notes?"

User: "Schedule a call with John for next Tuesday afternoon"
Assistant:
- Check calendar for Tuesday afternoon
- Suggest specific available times
- Once confirmed, create calendar event
- Offer to send invitation email
- Confirm: "Meeting scheduled for Tuesday at 2 PM. Would you like me to send John an invitation email?"

User: "What did Michael say about the market downturn?"
Assistant:
- Search emails from Michael mentioning market/downturn
- Read relevant emails
- Summarize Michael's comments
- Provide email dates for reference
- Suggest: "Would you like me to log this in his CRM notes for future reference?"

IMPORTANT NOTES:
- Always confirm before sending emails or creating events with attendees
- If unclear, ask questions rather than assume
- Provide source attribution (email dates, CRM timestamps)
- Suggest follow-up actions when appropriate
- Keep responses organized and scannable

Remember: You are empowering financial advisors to build stronger client relationships through better information management and organization. Every interaction should add value and save time.
"""


def create_financial_advisor_agent(
    model_name: str = "claude-sonnet-4-20250514",
    thread_id: Optional[str] = None
) -> Any:
    """
    Create the main Financial Advisor AI Agent

    Args:
        model_name: Claude model to use (default: claude-sonnet-4-20250514)
        thread_id: Optional thread ID for conversation persistence

    Returns:
        Configured DeepAgents agent graph
    """
    # Initialize Claude model
    llm = ChatAnthropic(
        model=model_name,
        api_key=settings.ANTHROPIC_API_KEY,
        temperature=0,  # Deterministic for consistency
        max_tokens=4096
    )

    # Combine all tools
    all_tools = gmail_tools + calendar_tools + hubspot_tools + rag_tools

    # Define subagents
    subagents = [
        email_researcher_agent(),
        calendar_scheduler_agent(),
        hubspot_manager_agent()
    ]

    # Checkpointer is optional; leave as None if unavailable or not configured
    checkpointer = None

    # Create agent graph using DeepAgents
    agent = create_deep_agent(
        model=llm,
        tools=all_tools,
        system_prompt=FINANCIAL_ADVISOR_AGENT_INSTRUCTIONS,
        subagents=subagents,
        checkpointer=checkpointer
    )

    logger.info(f"Created financial advisor agent with model: {model_name}")

    return agent


def invoke_agent(
    agent: Any,
    message: str,
    thread_id: str,
    user_id: str
) -> Dict[str, Any]:
    """
    Invoke the agent with a message

    Args:
        agent: Configured agent graph
        message: User message
        thread_id: Thread ID for conversation persistence
        user_id: User ID string for authentication

    Returns:
        Dict with agent response
    """
    try:
        # Prepare config with thread_id and user_id
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id
            }
        }

        # Invoke agent
        result = agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config=config
        )

        return result

    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        raise


def stream_agent(
    agent: Any,
    message: str,
    thread_id: str,
    user_id: str
):
    """
    Stream agent responses

    Args:
        agent: Configured agent graph
        message: User message
        thread_id: Thread ID for conversation persistence
        user_id: User ID string for authentication

    Yields:
        Agent response chunks
    """
    try:
        # Prepare config
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id
            }
        }

        # Stream agent responses
        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": message}]},
            config=config,
            stream_mode="values"
        ):
            yield chunk

    except Exception as e:
        logger.error(f"Error streaming agent: {e}")
        raise


# Example usage
if __name__ == "__main__":
    # This is for testing purposes only
    print("Creating Financial Advisor Agent...")

    agent = create_financial_advisor_agent()

    print("Agent created successfully!")
    print("\nAgent capabilities:")
    print("- Email research and analysis")
    print("- Calendar management and scheduling")
    print("- CRM contact and note management")
    print("- Multi-tool orchestration")
    print("- Subagent delegation")
