from langchain.agents import create_agent
from deepagents.middleware import (
    PlanningMiddleware,
    FilesystemMiddleware,
    SubAgentMiddleware,
)
from deepagents.state import AgentState
from langchain_core.tools import tool
from langchain.agents.middleware import AgentMiddleware
from typing import Annotated
from langgraph.prebuilt import InjectedState

SAMPLE_MODEL = "claude-3-5-sonnet-20240620"

class SampleState(AgentState):
    sample_input: str

@tool(description="Sample tool")
def sample_tool(sample_input: str):
    return sample_input

@tool(description="Sample tool with injected state")
def sample_tool_with_injected_state(sample_input: str, state: Annotated[dict, InjectedState]):
    return sample_input + state["sample_input"]

class SampleMiddlewareWithTools(AgentMiddleware):
    tools = [sample_tool]

class SampleMiddlewareWithToolsAndState(AgentMiddleware):
    state_schema = SampleState
    tools = [sample_tool]

class TestAddMiddleware:
    def test_planning_middleware(self):
        middleware = [PlanningMiddleware()]
        agent = create_agent(model=SAMPLE_MODEL, middleware=middleware, tools=[])
        assert "todos" in agent.stream_channels
        assert "write_todos" in agent.nodes["tools"].bound._tools_by_name.keys()

    def test_filesystem_middleware(self):
        middleware = [FilesystemMiddleware()]
        agent = create_agent(model=SAMPLE_MODEL, middleware=middleware, tools=[])
        assert "files" in agent.stream_channels
        agent_tools = agent.nodes["tools"].bound._tools_by_name.keys()
        assert "ls" in agent_tools
        assert "read_file" in agent_tools
        assert "write_file" in agent_tools
        assert "edit_file" in agent_tools

    def test_subagent_middleware(self):
        middleware = [
            SubAgentMiddleware(
                tools=[],
                subagents=[],
                model=SAMPLE_MODEL
            )
        ]
        agent = create_agent(model=SAMPLE_MODEL, middleware=middleware, tools=[])
        assert "task" in agent.nodes["tools"].bound._tools_by_name.keys()

    def test_multiple_middleware(self):
        middleware = [
            PlanningMiddleware(),
            FilesystemMiddleware(),
            SubAgentMiddleware(
                tools=[],
                subagents=[],
                model=SAMPLE_MODEL
            )
        ]
        agent = create_agent(model=SAMPLE_MODEL, middleware=middleware, tools=[])
        assert "todos" in agent.stream_channels
        assert "files" in agent.stream_channels
        agent_tools = agent.nodes["tools"].bound._tools_by_name.keys()
        assert "write_todos" in agent_tools
        assert "ls" in agent_tools
        assert "read_file" in agent_tools
        assert "write_file" in agent_tools
        assert "edit_file" in agent_tools
        assert "task" in agent_tools

    def test_sample_middleware(self):
        middleware = [SampleMiddlewareWithToolsAndState()]
        agent = create_agent(model=SAMPLE_MODEL, middleware=middleware, tools=[])
        assert "sample_input" in agent.stream_channels