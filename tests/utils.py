from langchain_core.tools import tool
from langchain.agents.middleware import AgentMiddleware
from typing import Annotated
from langchain.agents.tool_node import InjectedState
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

###########################
# Mock tools and middleware
###########################

SAMPLE_MODEL = "claude-3-5-sonnet-20240620"

@tool(description="Use this tool to get the weather")
def get_weather(location: str):
    return f"The weather in {location} is sunny."

@tool(description="Use this tool to get the latest soccer scores")
def get_soccer_scores(team: str):
    return f"The latest soccer scores for {team} are 2-1."

@tool(description="Sample tool")
def sample_tool(sample_input: str):
    return sample_input

@tool(description="Sample tool with injected state")
def sample_tool_with_injected_state(sample_input: str, state: Annotated[dict, InjectedState]):
    return sample_input + state["sample_input"]

class SampleMiddlewareWithTools(AgentMiddleware):
    tools = [sample_tool]

class SampleState(AgentState):
    sample_input: str

class SampleMiddlewareWithToolsAndState(AgentMiddleware):
    state_schema = SampleState
    tools = [sample_tool]

class WeatherToolMiddleware(AgentMiddleware):
    tools = [get_weather]
