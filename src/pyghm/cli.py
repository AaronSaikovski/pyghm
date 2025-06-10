#!/usr/bin/env python3

import click

from pyghm.config import GITHUB_TOKEN
from pyghm.github_utils import create_environment, get_repo
from pyghm.secrets import create_env_secret, delete_env_secret, update_env_secret
from pyghm.variables import (
    create_env_variable,
    delete_env_variable,
    environment_variable_exists,
    list_environment_variables,
    update_env_variable,
)

################################################
###(Main CLI Entry Point)
################################################


# ******************************************************************************** #
@click.group()
def cli():
    """GitHub Actions Environment CLI"""
    pass


# ******************************************************************************** #


@cli.command("get-repo")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def get_repo_cmd(repo, token):
    r = get_repo(token, repo)
    click.echo(f"📘 Repo: {r.full_name}, Private: {r.private}")


# ******************************************************************************** #


@cli.command("create-env")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def create_env_cmd(repo, env, token):
    r = get_repo(token, repo)
    create_environment(r, env)


# ******************************************************************************** #


@cli.command("create-var")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Variable name")
@click.option("--value", required=True, help="Variable value")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def create_var_cmd(repo, env, name, value, token):
    owner, repo_name = repo.split("/")
    create_env_variable(owner, repo_name, env, name, value, token)


# ******************************************************************************** #


@cli.command("update-var")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Variable name")
@click.option("--value", required=True, help="Variable value")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def update_var_cmd(repo, env, name, value, token):
    owner, repo_name = repo.split("/")
    update_env_variable(owner, repo_name, env, name, value, token)


# ******************************************************************************** #


@cli.command("create-secret")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Secret name")
@click.option("--value", required=True, help="Secret value")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def create_secret_cmd(repo, env, name, value, token):
    owner, repo_name = repo.split("/")
    create_env_secret(owner, repo_name, env, name, value, token)


# ******************************************************************************** #


@cli.command("delete-secret")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Secret name")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def delete_secret_cmd(repo, env, name, token):
    owner, repo_name = repo.split("/")
    delete_env_secret(owner, repo_name, env, name, token)


# ******************************************************************************** #


@cli.command("update-secret")
@click.option("--repo", required=True, help="Repository in owner/name format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Secret name")
@click.option("--value", required=True, help="Secret value")
def update_secret(repo, env, name, value):
    """Update an existing GitHub Actions environment variable."""
    if not GITHUB_TOKEN:
        raise click.ClickException("GITHUB_TOKEN environment variable not set.")
    owner, repo_name = repo.split("/")
    update_env_secret(owner, repo_name, env, name, value, GITHUB_TOKEN)


# ******************************************************************************** #


@cli.command("delete-var")
@click.option("--repo", required=True, help="Repository in owner/name format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Variable name")
def delete_var(repo, env, name):
    """Delete a GitHub Actions environment variable."""
    if not GITHUB_TOKEN:
        raise click.ClickException("GITHUB_TOKEN is not set.")
    owner, repo_name = repo.split("/")
    delete_env_variable(owner, repo_name, env, name, GITHUB_TOKEN)


# ******************************************************************************** #


@cli.command("check-var")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--name", required=True, help="Variable name to check")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def check_var_cmd(repo, env, name, token):
    """Check if a GitHub Actions environment variable exists."""
    owner, repo_name = repo.split("/")
    try:
        exists = environment_variable_exists(owner, repo_name, env, name, token)
        if exists:
            click.echo(f"✅ Variable '{name}' exists in environment '{env}'.")
        else:
            click.echo(f"❌ Variable '{name}' does NOT exist in environment '{env}'.")
    except Exception as e:
        raise click.ClickException(f"Error checking variable existence: {e}")


# ******************************************************************************** #
@cli.command("list-vars")
@click.option("--repo", required=True, help="Repository in 'owner/repo' format")
@click.option("--env", required=True, help="Environment name")
@click.option("--token", envvar="GITHUB_TOKEN", required=True, help="GitHub token")
def list_vars_cmd(repo, env, token):
    """List environment variables names for a GitHub Actions environment."""
    owner, repo_name = repo.split("/")
    try:
        variables = list_environment_variables(owner, repo_name, env, token)
        if variables:
            click.echo(f"Variables in '{env}':")
            for var in variables:
                click.echo(f"- {var['name']}")
        else:
            click.echo(f"No variables found in environment '{env}'.")
    except Exception as e:
        raise click.ClickException(f"Error listing variables: {e}")


# ******************************************************************************** #
if __name__ == "__main__":
    cli()

# ******************************************************************************** #
