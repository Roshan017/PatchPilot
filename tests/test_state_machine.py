from patchpilot.state_machine import (
    AgentState,
    AgentStateMachine,
)

import pytest

@pytest.mark.parametrize(
    ("current_state", "next_state"),

    [
        (AgentState.RECEIVED, AgentState.COMPLETED),
        (AgentState.RECEIVED, AgentState.FAILED),
        (AgentState.COMPLETED, AgentState.ANALYZING),
        (AgentState.FAILED, AgentState.ANALYZING),
        (AgentState.COMPLETED, AgentState.FAILED)
    ]
)

def test_invalid_transitions_are_rejected(current_state, next_state):
    agent = AgentStateMachine()

    agent.state = current_state

    with pytest.raises(ValueError):
        agent.transition(next_state)
    
    assert agent.state == current_state


def test_agent_starts_in_received_state():
    agent = AgentStateMachine()

    assert agent.state == AgentState.RECEIVED


def test_agent_can_transition_to_analyzing():
    agent = AgentStateMachine()

    agent.transition(AgentState.ANALYZING)

    assert agent.state == AgentState.ANALYZING


def test_agent_rejects_invalid_transition():
    agent = AgentStateMachine()

    try:
        agent.transition(AgentState.COMPLETED)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid transition should raise ValueError")