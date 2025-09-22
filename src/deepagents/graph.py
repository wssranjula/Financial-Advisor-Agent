from typing import Sequence, Union, Callable, Any, TypeVar, Type, Optional
from langchain_core.tools import BaseTool
from langchain_core.language_models import LanguageModelLike
from langgraph.types import Checkpointer
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, SummarizationMiddleware, HumanInTheLoopMiddleware
from langchain.agents.middleware.human_in_the_loop import ToolConfig
from langchain.agents.middleware.prompt_caching import AnthropicPromptCachingMiddleware
from langchain.chat_models import init_chat_model
from langchain_anthropic import ChatAnthropic
from deepagents.middleware import PlanningMiddleware, FilesystemMiddleware, SubAgentMiddleware
from deepagents.prompts import BASE_AGENT_PROMPT
from deepagents.model import get_default_model
from deepagents.state import DeepAgentState
from deepagents.types import SubAgent, CustomSubAgent

StateSchema = TypeVar("StateSchema", bound=DeepAgentState)
StateSchemaType = Type[StateSchema]

def agent_builder(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]],
    instructions: str,
    middleware: list[AgentMiddleware] = [],
    tool_configs: Optional[dict[str, bool | ToolConfig]] = None,
    model: Optional[Union[str, LanguageModelLike]] = None,
    subagents: list[SubAgent | CustomSubAgent] = None,
    context_schema: Optional[Type[Any]] = None,
    checkpointer: Optional[Checkpointer] = None,
    is_async: bool = False,
):
    if model is None:
        model = get_default_model()
    elif isinstance(model, str):
        model = init_chat_model(model)

    deepagent_middleware = [
        PlanningMiddleware(),
        FilesystemMiddleware(),
        SubAgentMiddleware(
            tools=tools,
            subagents=subagents,
            model=model,
            is_async=is_async,
        ),
        SummarizationMiddleware(
            model=model,
            max_tokens_before_summary=20000,    # NOTE: To tweak
            messages_to_keep=20,
        ),
        *middleware,
    ]
    # Add tool interrupt config if provided
    if tool_configs is not None:
        deepagent_middleware.append(HumanInTheLoopMiddleware(tool_configs=tool_configs))

    # Add Anthropic prompt caching is model is Anthropic
    # if isinstance(model, ChatAnthropic):
    #     deepagent_middleware.append(AnthropicPromptCachingMiddleware(ttl="5m"))

    return create_agent(
        model,
        prompt=instructions + "\n\n" + BASE_AGENT_PROMPT,
        tools=tools,
        middleware=deepagent_middleware,
        context_schema=context_schema,
        checkpointer=checkpointer,
    )

def create_deep_agent(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]] = [],
    instructions: str = "",
    middleware: list[AgentMiddleware] = [],
    model: Optional[Union[str, LanguageModelLike]] = None,
    subagents: list[SubAgent | CustomSubAgent] = [],
    context_schema: Optional[Type[Any]] = None,
    checkpointer: Optional[Checkpointer] = None,
    tool_configs: Optional[dict[str, bool | ToolConfig]] = None,
):
    return agent_builder(
        tools=tools,
        instructions=instructions,
        middleware=middleware,
        model=model,
        subagents=subagents,
        context_schema=context_schema,
        checkpointer=checkpointer,
        tool_configs=tool_configs,
        is_async=False,
    )

def async_create_deep_agent(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]] = [],
    instructions: str = "",
    middleware: list[AgentMiddleware] = [],
    model: Optional[Union[str, LanguageModelLike]] = None,
    subagents: list[SubAgent | CustomSubAgent] = [],
    context_schema: Optional[Type[Any]] = None,
    checkpointer: Optional[Checkpointer] = None,
    tool_configs: Optional[dict[str, bool | ToolConfig]] = None,
):
    return agent_builder(
        tools=tools,
        instructions=instructions,
        middleware=middleware,
        model=model,
        subagents=subagents,
        context_schema=context_schema,
        checkpointer=checkpointer,
        tool_configs=tool_configs,
        is_async=True,
    )