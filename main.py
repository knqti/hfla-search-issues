import ast
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from ghapi.all import GhApi

def get_credentials():
    load_dotenv()
    credential = os.getenv('GITHUB_TOKEN')
    
    return credential

def get_repos(csv_file:str):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        list_of_repos = []

        for row in reader:
            repository_url = row[0]
            # Get repo name at the end of URL
            repository_name = repository_url.split('.com/')[1]
            list_of_repos.append(repository_name)
     
    return list_of_repos

def search_issues(repository:str, search_term:str):
    query = f'repo:{repository} is:issue {search_term}'
    
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

def parse_issues(api_response:dict, repo:str, keywords:str):
    issues_count = api_response['total_count']
    parsed_data = []

    for issue in api_response['items']:
        # Remove parenthesis, aposterphe, and comma
        issue_title = issue['title'].strip("()',")
        issue_url = issue['html_url']
        issue_number = issue['number']
        parsed_data.append((repo, keywords, issue_title, issue_url, issue_number))
        
    return issues_count, parsed_data

def export_to_csv(file_name:str, list_name:str):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(list_name)

if __name__ == '__main__':
    now = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    
    if os.path.exists('.env'):
        token = get_credentials()
        api = GhApi(token)
    else:
        api = GhApi()
    
    repo_urls = './repo_urls.csv'
    repo_list = get_repos(repo_urls)

    keywords = input('Keywords to search for: ').lower().strip()
    keywords_quoted = f'"{keywords}"'
    keywords_hyphened = keywords.replace(' ', '-')

    issues_list = [('Repository', 'Keywords', 'Issue Title', 'Issue URL', 'Issue Number')]
    no_issues_list = []

    issues_output_file = f'{now}_issues_{keywords_hyphened}.csv'
    no_issues_output_file = f'{now}_no-issues_{keywords_hyphened}.csv'

    for repo in repo_list:
        print(f'Searching {repo}...')

        try:
            response_dict = search_issues(repo, keywords_quoted)
            total_issues, data_list = parse_issues(response_dict, repo, keywords)

            if total_issues == 0:
                message = [f'No issues in repo "{repo}" with keywords "{keywords}".']
                no_issues_list.append(message)
            else:
                issues_list.extend(data_list)

        except Exception as e:
            print(f'Error with repo {repo}: {e}')

    export_to_csv(issues_output_file, issues_list)
    export_to_csv(no_issues_output_file, no_issues_list)
    
    print(f'Done! Output files ready: \n{issues_output_file}\n{no_issues_output_file}')
