import requests

# GitHub Configuration
GITHUB_ORG = 'your_github_org'  # Replace with your GitHub organization name
GITHUB_TOKEN = 'your_github_token'  # Replace with your GitHub personal access token
GITHUB_USERNAME = 'your_github_username'  # Replace with your GitHub username

# Gitea Configuration
GITEA_URL = 'https://your_gitea_instance/api/v1'  # Base URL of your Gitea instance's API
GITEA_TOKEN = 'your_gitea_token'  # Replace with your Gitea API token
GITEA_USERNAME = 'your_gitea_username'  # Replace with your Gitea username
GITEA_ORG = 'your_gitea_org'  # Replace with your Gitea organization name

# Function to get all repos from a GitHub organization
def get_github_repos(org_name):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    repos = []
    page = 1
    while True:
        response = requests.get(f'https://api.github.com/orgs/{org_name}/repos', headers=headers, params={'page': page, 'per_page': 100})
        if response.status_code != 200:
            print(f"Error fetching repos: {response.json()}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

# Function to migrate a repo from GitHub to Gitea using the /repos/migrate API
def migrate_repo_to_gitea(repo):
    repo_name = repo['name']
    repo_clone_url = repo['clone_url']
    default_branch = repo['default_branch']
    is_private = repo['private']

    headers = {'Authorization': f'token {GITEA_TOKEN}'}
    payload = {
        'clone_addr': repo_clone_url,
        'repo_name': repo_name,
        'mirror': False,
        'private': is_private,
        'auth_username': GITHUB_USERNAME,
        'auth_token': GITHUB_TOKEN,
        'wiki': True,
        'issues': True,
        'labels': True,
        'milestones': True,
        'pull_requests': True,
        'releases': True,
        'repo_owner': GITEA_ORG,
    }

    response = requests.post(f'{GITEA_URL}/repos/migrate', headers=headers, json=payload)
    if response.status_code == 201:
        print(f'Repo {repo_name} successfully migrated to Gitea.')
    else:
        print(f'Error migrating repo {repo_name}: {response.json()}')

# Main function to migrate all repos
def migrate_all_repos():
    repos = get_github_repos(GITHUB_ORG)
    for repo in repos:
        migrate_repo_to_gitea(repo)

if __name__ == '__main__':
    migrate_all_repos()
