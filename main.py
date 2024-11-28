import ast
import csv
from ghapi.all import GhApi
from token_file import GITHUB_TOKEN

def search_issues(repository:str, search_term:str):
    query = f'repo:hackforla/{repository} is:issue {search_term}'
    
    results = api.search.issues_and_pull_requests(
        q=query,
        sort=None,
        order=None,
        per_page=None,
        page=None
    )

    # Use `ast` to parse results into Python
    results_dict = ast.literal_eval(str(results))
    return results_dict

def parse_issues(api_response:dict):
    issues_count = api_response['total_count']
    
    list_of_titles = []
    list_of_urls = []
    list_of_numbers = []

    for issue in api_response['items']:
        issue_title = issue['title'].strip("()',")
        list_of_titles.append(issue_title)
        
        issue_url = issue['html_url']
        list_of_urls.append(issue_url)

        issue_number = issue['number']
        list_of_numbers.append(issue_number)
        
    return issues_count, list_of_titles, list_of_urls, list_of_numbers


if __name__ == '__main__':
    api = GhApi(token=GITHUB_TOKEN)

    repo = input('Repo to search in: ').lower().strip()
    keywords = input('Keywords to search for: ').lower().strip()

    issues_dict = search_issues(repo, keywords)
    issues_found, titles, urls, numbers = parse_issues(issues_dict)

    if issues_found == 0:
        print(f'No issues found in repo {repo} with keywords "{keywords}".')
    else:
        data = [['Repo', 'Title', 'URL', 'Issue Number']]

        for title, url, number in zip(titles, urls, numbers):
            data.append([repo, title, url, number])
        
        with open(f'issues_{repo}_{keywords}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data) 
