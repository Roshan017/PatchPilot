from patchpilot.context import AgentContext

def test_context_store_bug_report_and_repository():

    context = AgentContext(
        bug_report="Login fails with special chars",
        repository_path="./sample-repo"
    )

    assert context.bug_report == "Login fails with special chars"


    assert context.repository_path == "./sample-repo"


def test_context_fields_start_empty():

    context = AgentContext(
        bug_report= "Login failure",
        repository_path="./sample-repo",
    )

    assert context.investigation is None
    assert context.patch is None
    assert context.test_results == {}
    assert context.error is None


def test_context_test_results_are_independent():
        
    first = AgentContext("Bug A", "./repo-a")
    second = AgentContext("Bug B", "./repo-b")

    first.test_results["passed"] = True

    assert second.test_results == {}
    

