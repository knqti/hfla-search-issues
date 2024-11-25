from ghapi.all import GhApi
from token_file import GITHUB_TOKEN

api = GhApi(token=GITHUB_TOKEN)

issues = api.issues.list_for_repo(
    owner='hackforla',
    repo='knowledgebase-content',
    labels='Complexity: Extra Large'
)

for issue in issues:
    print(f"{issue.title} - {issue.html_url}")
