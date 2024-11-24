import responses
from jira_data_library.api import JiraAPI

@responses.activate
def test_get_issue_details():
    api = JiraAPI("https://example.atlassian.net/rest/api/3", "user", "token")
    responses.add(
        responses.GET,
        "https://example.atlassian.net/rest/api/3/issue/TEST-123",
        json={"key": "TEST-123", "fields": {"summary": "Test issue"}},
        status=200
    )

    response = api.get("issue/TEST-123")
    assert response["key"] == "TEST-123"
