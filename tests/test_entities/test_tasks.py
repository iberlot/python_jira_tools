import responses
from jira_data_library.api import JiraAPI
from jira_data_library.entities.tasks import JiraTasks

@responses.activate
def test_get_task():
    api = JiraAPI("https://example.atlassian.net/rest/api/3", "user", "token")
    tasks = JiraTasks(api)

    responses.add(
        responses.GET,
        "https://example.atlassian.net/rest/api/3/issue/TEST-123",
        json={"key": "TEST-123", "fields": {"summary": "Test Task"}},
        status=200
    )

    task = tasks.get_task("TEST-123")
    assert task["key"] == "TEST-123"
    assert task["fields"]["summary"] == "Test Task"
