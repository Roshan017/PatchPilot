import pytest
from patchpilot.context import AgentContext
from patchpilot.state_machine import AgentState
from patchpilot.workflow import run_workflow



def test_workflow_completes_succesfully():

    context = AgentContext(
        bug_report= "Test Bug",
        repository_path="./sample-repo"
    )


    final_state = run_workflow(context)

    assert final_state == AgentState.COMPLETED

    