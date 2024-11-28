import ast
import csv
from ghapi.all import GhApi
from token_file import GITHUB_TOKEN

def get_repos(csv_file:str):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        list_of_repos = []

        for repo_url in reader:
            # Get repo name at the end of URL
            repo_name = repo_url[0]
            repo_name = repo_name.split(".com/")[1]
            list_of_repos.append(repo_name)
        
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

def parse_issues(api_response:dict):
    issues_count = api_response['total_count']
    parsed_data = [('issue_title', 'issue_url', 'issue_number')]

    for issue in api_response['items']:
        # Remove parenthesis, aposterphe, and comma
        issue_title = issue['title'].strip("()',")
        issue_url = issue['html_url']
        issue_number = issue['number']
        parsed_data.append((issue_title, issue_url, issue_number))
        
    return issues_count, parsed_data


if __name__ == '__main__':
    api = GhApi(token=GITHUB_TOKEN)
    
    repo_urls = './repo_urls.csv'
    repo_list = get_repos(repo_urls)

    keywords = input('Keywords to search for: ').lower().strip()
    keywords = '"' + keywords + '"'

    for repo in repo_list:
        try:
            response_dict = search_issues(repo, keywords)
            total_issues, data_list = parse_issues(response_dict)

            if total_issues == 0:
                print(f'No issues in repo "{repo}" with keywords "{keywords}".')
            else:
                new_repo_str = str(repo.replace('/', '-'))
                new_keywords_str = str(keywords.strip('"'))
                output_file = f'issues_{new_repo_str}_{new_keywords_str}.csv'

                with open(output_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(data_list)
                    print(f'Success! {output_file}')

        except Exception as e:
            print(f'Error: {e}')
