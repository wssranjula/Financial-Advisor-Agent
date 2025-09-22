from deepagents.builder import create_configurable_agent
from tests.utils import assert_all_deepagent_qualities, get_weather, sample_tool, get_soccer_scores

SAMPLE_MODEL = "claude-3-5-sonnet-20240620"

class TestConfigurableAgent:
    def test_configurable_agent(self):
        # This creates a builder for configurable agents.
        builder = create_configurable_agent(
            default_instructions="You are a helpful assistant who loves researching things.",
            default_sub_agents=[
                {
                    "name": "weather_agent",
                    "description": "Use this agent to get the weather",
                    "prompt": "You are a weather agent.",
                    "tools": ["get_weather"],
                    "model": SAMPLE_MODEL,

                }
            ],
            # This is the global list of tools that can be used by the main agent or the subagent.
            tools=[sample_tool, get_weather, get_soccer_scores],
        )
        config = {
            "configurable" : {
                "instructions": "You are a helpful assistant who loves researching things.",
                "tools": ["sample_tool"]
            }
        }
        agent = builder(config)
        assert_all_deepagent_qualities(agent)
        result = agent.invoke({"messages": [{"role": "user", "content": "Get the weather in New York."}]})
        agent_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
        tool_calls = [tool_call for msg in agent_messages for tool_call in msg.tool_calls]
        assert any([tool_call["name"] == "task" and tool_call["args"].get("subagent_type") == "weather_agent" for tool_call in tool_calls])


    def test_configurable_agent_with_subagents(self):
        # This creates a builder for configurable agents.
        builder = create_configurable_agent(
            default_instructions="You are a helpful assistant who loves researching things.",
            default_sub_agents=[
                {
                    "name": "weather_agent",
                    "description": "Use this agent to get the weather",
                    "prompt": "You are a weather agent.",
                    "tools": ["get_weather"],
                    "model": SAMPLE_MODEL,

                }
            ],
            # This is the global list of tools that can be used by the main agent or the subagent.
            tools=[sample_tool, get_weather, get_soccer_scores],
        )
        config = {
            "configurable" : {
                "instructions": "You are a helpful assistant who loves researching things.",
                "subagents": [
                    {
                        "name": "soccer_agent",
                        "description": "Use this agent to get the latest soccer scores",
                        "prompt": "You are a soccer agent.",
                        "tools": ["get_soccer_scores"],
                    }
                ],
                "tools": ["sample_tool"]
            }
        }
        agent = builder(config)
        assert_all_deepagent_qualities(agent)
        result = agent.invoke({"messages": [{"role": "user", "content": "Get the latest soccer scores for Manchester City."}]})
        agent_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
        tool_calls = [tool_call for msg in agent_messages for tool_call in msg.tool_calls]
        assert any([tool_call["name"] == "task" and tool_call["args"].get("subagent_type") == "soccer_agent" for tool_call in tool_calls])

    def test_undefined_tools(self):
        builder = create_configurable_agent(
            default_instructions="You are a helpful assistant who loves researching things.",
            default_sub_agents=[
                {
                    "name": "weather_agent",
                    "description": "Use this agent to get the weather",
                    "prompt": "You are a weather agent.",
                    "tools": ["get_weather"],
                    "model": SAMPLE_MODEL,

                }
            ],
            # This is the global list of tools that can be used by the main agent or the subagent.
            tools=[sample_tool, get_weather, get_soccer_scores],
        )
        config = {
            "configurable" : {
                "instructions": "You are a helpful assistant who loves researching things.",
                "subagents": [
                    {
                        "name": "soccer_agent",
                        "description": "Use this agent to get the latest soccer scores",
                        "prompt": "You are a soccer agent.",
                        "tools": ["get_soccer_scores", "bad_tool_2"],
                    }
                ],
                "tools": ["sample_tool", "bad_tool_1"]
            }
        }
        agent = builder(config)
        assert_all_deepagent_qualities(agent)
        result = agent.invoke({"messages": [{"role": "user", "content": "Get the latest soccer scores for Manchester City."}]})
        agent_messages = [msg for msg in result.get("messages", []) if msg.type == "ai"]
        tool_calls = [tool_call for msg in agent_messages for tool_call in msg.tool_calls]
        assert any([tool_call["name"] == "task" and tool_call["args"].get("subagent_type") == "soccer_agent" for tool_call in tool_calls])