from deepagents.graph import create_deep_agent
from langchain_core.tools import tool
from langchain.agents.middleware import AgentMiddleware
from typing import Annotated
from langgraph.prebuilt import InjectedState
from langchain.agents.middleware import AgentMiddleware, AgentState

def assert_all_deepagent_qualities(agent):
    assert "todos" in agent.stream_channels
    assert "files" in agent.stream_channels
    assert "write_todos" in agent.nodes["tools"].bound._tools_by_name.keys()
    assert "ls" in agent.nodes["tools"].bound._tools_by_name.keys()
    assert "read_file" in agent.nodes["tools"].bound._tools_by_name.keys()
    assert "write_file" in agent.nodes["tools"].bound._tools_by_name.keys()
    assert "edit_file" in agent.nodes["tools"].bound._tools_by_name.keys()
    assert "task" in agent.nodes["tools"].bound._tools_by_name.keys()

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

class TestDeepAgents:
    def test_base_deep_agent(self):
        agent = create_deep_agent()
        assert_all_deepagent_qualities(agent)

    def test_deep_agent_with_tool(self):
        agent = create_deep_agent(tools=[sample_tool])
        assert_all_deepagent_qualities(agent)
        assert "sample_tool" in agent.nodes["tools"].bound._tools_by_name.keys()

    def test_deep_agent_with_middleware_with_tool(self):
        agent = create_deep_agent(middleware=[SampleMiddlewareWithTools()])
        assert_all_deepagent_qualities(agent)
        assert "sample_tool" in agent.nodes["tools"].bound._tools_by_name.keys()

    def test_deep_agent_with_middleware_with_tool_and_state(self):
        agent = create_deep_agent(middleware=[SampleMiddlewareWithToolsAndState()])
        assert_all_deepagent_qualities(agent)
        assert "sample_tool" in agent.nodes["tools"].bound._tools_by_name.keys()
        assert "sample_input" in agent.stream_channels

    def test_deep_agent_with_subagents(self):
        pass
