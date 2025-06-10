import click
import httpx

from pyghm.config import GITHUB_REPO_URL

# ******************************************************************************** #


def create_env_variable(owner, repo_name, env_name, var_name, var_value, token) -> int:
    """Create a GitHub Actions environment variable.

    Args:
        owner (_type_): _description_
        repo_name (_type_): _description_
        env_name (_type_): _description_
        var_name (_type_): _description_
        var_value (_type_): _description_
        token (_type_): _description_
    """
    url = f"{GITHUB_REPO_URL}/{owner}/{repo_name}/environments/{env_name}/variables"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"name": var_name, "value": var_value}
    response = httpx.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        click.echo(f"✅ Environment variable '{var_name}' added.")
    else:
        click.echo(f"❌ Failed to add variable: {response.text}")

    return response.status_code


# ******************************************************************************** #


def update_env_variable(owner, repo_name, env_name, var_name, var_value, token):
    """Update an existing GitHub Actions environment variable.

    Args:
        owner (_type_): _description_
        repo_name (_type_): _description_
        env_name (_type_): _description_
        var_name (_type_): _description_
        var_value (_type_): _description_
        token (_type_): _description_
    """

    # First try to delete the variable if it exists
    delete_resp = delete_env_variable(owner, repo_name, env_name, var_name, token)
    if delete_resp == 204:
        print(f"🗑️ Deleted existing variable '{var_name}' before updating.")
    elif delete_resp == 404:
        print(f"ℹ️ Variable '{var_name}' did not exist, proceeding to create.")
    else:
        print(f"❌ Failed to delete variable before update: {delete_resp}")
        return

    create_resp = create_env_variable(
        owner, repo_name, env_name, var_name, var_value, token
    )

    if create_resp == 201:
        print(f"✅ Created environment variable '{var_name}'.")
    else:
        print(f"❌ Failed to create variable: {create_resp}")


# ******************************************************************************** #


def delete_env_variable(owner, repo_name, env_name, var_name, token) -> int:
    """
    Delete an environment variable from a GitHub Actions environment.

    Args:
        owner (str): Repository owner.
        repo_name (str): Repository name.
        env_name (str): Environment name.
        var_name (str): Environment variable name.
        token (str): GitHub personal access token.
    """
    url = f"{GITHUB_REPO_URL}/{owner}/{repo_name}/environments/{env_name}/variables/{var_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    response = httpx.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"✅ Deleted variable '{var_name}'.")
    elif response.status_code == 404:
        print(f"ℹ️ Variable '{var_name}' not found.")
    else:
        print(f"❌ Failed to delete variable: {response.status_code} {response.text}")
    return response.status_code


# ******************************************************************************** #


def environment_variable_exists(owner, repo_name, env_name, var_name, token) -> bool:
    """Check if a GitHub Actions environment variable exists.

    Args:
        owner (_type_): _description_
        repo_name (_type_): _description_
        env_name (_type_): _description_
        var_name (_type_): _description_
        token (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        bool: _description_
    """
    url = f"{GITHUB_REPO_URL}/{owner}/{repo_name}/environments/{env_name}/variables"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    response = httpx.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch variables: {response.status_code} {response.text}"
        )

    variables = response.json().get("variables", [])
    return any(var["name"] == var_name for var in variables)


# ******************************************************************************** #


def list_environment_variables(owner, repo_name, env_name, token):
    url = f"{GITHUB_REPO_URL}/{owner}/{repo_name}/environments/{env_name}/variables"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    response = httpx.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch variables: {response.status_code} {response.text}"
        )
    return response.json().get("variables", [])


# ******************************************************************************** #
