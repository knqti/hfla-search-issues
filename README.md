# Overview

[Hack for LA Guides](https://github.com/hackforla/guides) members gather examples from [GitHub issues](https://github.com/hackforla/guides/wiki/Gathering-Examples-with-Github) as part of the initial guide-making process. 

`hfla-search-issues` is a Python script that searches for issues within GitHub repositories. It uses the Python client, [`ghapi`](https://ghapi.fast.ai/), to access [GitHub's REST API](https://docs.github.com/en/rest?apiVersion=2022-11-28). 

The script does the following:

1. Asks for keywords to search for
2. Loops through a CSV file of repositories
3. Calls the API for issues within each repository
4. Outputs two CSV file when finished: 
   a. Repositories with issues found
   b. Repositories with no issues found

# How to Use

Follow the steps below to use `hfla-search-issues`.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- Access to your computer's terminal

> Note: The terminal commands below are in bash.

## Download

To download a copy:

1. At the top of this repository, click the Code button
2. Click Download ZIP
3. Extract the zipped folder

> Note: If you use the Download ZIP option, the folder will have the branch name added to the end.

To clone this repository, run the following command in your terminal:

```bash
git clone https://github.com/knqti/hfla-search-issues.git
```

## Change directory 

Navigate into `hfla-search-issues`' root directory:

```bash
cd /PATH/TO/hfla-search-issues
```

## Dependencies

Install dependencies from *requirements.txt*:

```bash
pip install -r ./requirements.txt
```

## Personal access token (optional)

A GitHub personal access token is optional, but recommended. Using a token increases API rate limits and access to restricted repositories you would otherwise need to log into.

To create a token, see [Managing your personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#about-personal-access-tokens).

To use your token, create a *.env* file:

```bash
echo "GITHUB_TOKEN = 'YOUR_TOKEN_GOES_HERE'" > .env
```

## Run

To run `hfla-search-issues`:

```bash
python3 main.py
```

You are prompted with `Keywords to search for:`. Type your keywords and press enter. 

`hfla-search-issues` searches through the repository links in *repo_urls.csv*. Update the links as needed.

# API References

- `hfla-search-issues` calls `ghapi`'s method [`search.issues_and_pull_requests`](https://ghapi.fast.ai/fullapi.html)
- `search.issues_and_pull_requests` calls the API endpoint [Search issues and pull requests](https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-issues-and-pull-requests)
