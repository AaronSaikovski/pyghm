import base64

import click
import httpx
from nacl import encoding, public

from pyghm.config import GITHUB_REPO_URL

# ******************************************************************************** #


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a secret value using the given public key.

    Args:
        public_key (str): _description_
        secret_value (str): _description_

    Returns:
        str: _description_
    """
    key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


# ******************************************************************************** #


def create_env_secret(owner, repo_name, env_name, secret_name, secret_value, token):
    """Create a GitHub Actions environment secret.

    Args:
        owner (_type_): _description_
        repo_name (_type_): _description_
        env_name (_type_): _description_
        secret_name (_type_): _description_
        secret_value (_type_): _description_
        token (_type_): _description_
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    key_url = f"{GITHUB_REPO_URL}/{owner}/{repo_name}/environments/{env_name}/secrets/public-key"
    key_response = httpx.get(key_url, headers=headers)
    if key_response.status_code != 200:
        click.echo(f"❌ Failed to get public key: {key_response.text}")
        return

    key_data = key_response.json()
    key_id = key_data["key_id"]
    public_key = key_data["key"]

    encrypted_value = encrypt_secret(public_key, secret_value)

    secret_url = f"{GITHUB_REPO_URL}/{owner}/{repo_name}/environments/{env_name}/secrets/{secret_name}"
    payload = {"encrypted_value": encrypted_value, "key_id": key_id}
    r = httpx.put(secret_url, headers=headers, json=payload)
    if r.status_code in [201, 204]:
        click.echo(f"✅ Secret '{secret_name}' added.")
    else:
        click.echo(f"❌ Failed to add secret: {r.text}")


# ******************************************************************************** #
