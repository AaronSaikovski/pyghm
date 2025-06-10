import click
from github import Github

# ******************************************************************************** #


def get_repo(token: str, repo_name: str):
    """Get a GitHub repository.

    Args:
        token (str): _description_
        repo_name (str): _description_

    Returns:
        _type_: _description_
    """
    github = Github(token)
    return github.get_repo(repo_name)


# ******************************************************************************** #


def create_environment(repo, env_name: str):
    """Create a GitHub Actions environment.

    Args:
        repo (_type_): _description_
        env_name (str): _description_
    """
    existing_envs = repo.get_environments()
    if env_name not in [e.name for e in existing_envs]:
        repo.create_environment(environment_name=env_name)
        click.echo(f"✅ Created environment: {env_name}")
    else:
        click.echo(f"ℹ️ Environment '{env_name}' already exists")


# ******************************************************************************** #
