from langchain.agents import create_agent
from deepagents.state import AgentState
from typing import NotRequired 
from langchain.agents.middleware import AgentMiddleware

SAMPLE_MODEL = "claude-3-5-sonnet-20240620"

class SampleState(AgentState):
    sample_input: NotRequired[str]

class SampleMiddlewareWithState(AgentMiddleware):
    state_schema = SampleState

# class TestAddMiddleware:
#     def test_sample_middleware(self):
#         middleware = [SampleMiddlewareWithState()]
#         agent = create_agent(model=SAMPLE_MODEL, middleware=middleware, tools=[])
#         assert "sample_input" in agent.stream_channels

agent = create_agent(model=SAMPLE_MODEL, middleware=[SampleMiddlewareWithState()], tools=[])
print(agent.stream_channels)