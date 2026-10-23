from enum import Enum, auto 


class AgentState(Enum):
    RECEIVED = auto()
    ANALYZING = auto()
    FAILED = auto()
    COMPLETED = auto()


class AgentStateMachine:
    ALLOWED_TRANSITIONS = {
        AgentState.RECEIVED: {AgentState.ANALYZING},
        AgentState.ANALYZING: {
            AgentState.COMPLETED,
            AgentState.FAILED,
        },
        AgentState.COMPLETED: set(),
        AgentState.FAILED: set(),
    }

    def __init__(self):
        self.state = AgentState.RECEIVED

    def transition(self, new_state: AgentState) -> None:
        if new_state not in self.ALLOWED_TRANSITIONS[self.state]:
            raise ValueError(
                f"Invalid transition: {self.state.name} "
                f"-> {new_state.name}"
            )

        self.state = new_state


