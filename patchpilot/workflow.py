from patchpilot.context import AgentContext
from patchpilot.state_machine import AgentState, AgentStateMachine


def run_workflow(context: AgentContext) -> AgentState:

    state_machine = AgentStateMachine()

    try: 
        state_machine.transition(AgentState.ANALYZING)

        state_machine.transition(AgentState.COMPLETED)

    
    except Exception:
        if state_machine.state == AgentState.ANALYZING:
            state_machine.transition(AgentState.FAILED)
        raise

    return state_machine.state