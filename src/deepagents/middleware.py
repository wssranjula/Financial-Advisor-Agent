"""DeepAgents implemented as Middleware"""

from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest
from deepagents.state import Todo, file_reducer
from typing import NotRequired, Annotated
from deepagents.tools import write_todos, ls, read_file, write_file, edit_file
from deepagents.prompts import WRITE_TODOS_SYSTEM_PROMPT, TASK_SYSTEM_PROMPT, FILESYSTEM_SYSTEM_PROMPT
from deepagents.sub_agent import SubAgent, CustomSubAgent, _create_sync_task_tool, _create_task_tool


###############################
# Current Limitations
# - Prompts are segregated for each piece of middleware, no composition (write todos in subagents)
# - State Schema doesn't work right now!
# - Need to add back interrupt support!
###############################

class PlanningState(AgentState):
    todos: NotRequired[list[Todo]]

class PlanningMiddleware(AgentMiddleware):
    state_schema = PlanningState
    tools = [write_todos]

    def modify_model_request(self, request: ModelRequest, agent_state: AgentState) -> ModelRequest:
        print(request)
        request.system_prompt = request.system_prompt + "\n\n" + WRITE_TODOS_SYSTEM_PROMPT

    # TODO: Prune out more than one call of write_todos in parallel.
    # def after_model(self, state: AgentState) -> dict[str, Any] | None:
    #     return {
    #         "messages": [AIMessage(content="")]
    #     }

class FilesystemState(AgentState):
    files: Annotated[NotRequired[dict[str, str]], file_reducer]

class FilesystemMiddleware(AgentMiddleware):
    state_schema = FilesystemState
    tools = [ls, read_file, write_file, edit_file]

    def modify_model_request(self, request: ModelRequest, agent_state: AgentState) -> ModelRequest:
        request.system_prompt = request.system_prompt + "\n\n" + FILESYSTEM_SYSTEM_PROMPT

class SubAgentMiddleware(AgentMiddleware):
    def __init__(
        self,
        tools,
        instructions,
        subagents: list[SubAgent | CustomSubAgent],
        model,
        state_schema=None,
        is_async=False,
    ) -> None:
        super().__init__()
        if is_async:
            self.tools = [
                _create_task_tool(
                    tools=tools,
                    instructions=instructions,
                    subagents=subagents,
                    model=model,
                    state_schema=state_schema or None,
                )
            ]
        else:
            self.tools = [
                _create_sync_task_tool(
                    tools=tools,
                    instructions=instructions,
                    subagents=subagents,
                    model=model,
                    state_schema=state_schema or None,
                )
            ]

    def modify_model_request(self, request: ModelRequest, agent_state: AgentState) -> ModelRequest:
        request.system_prompt = request.system_prompt + "\n\n" + TASK_SYSTEM_PROMPT
