import os

from dotenv import load_dotenv

load_dotenv(override=True)  # This will force override existing env vars

# ******************************************************************************** #
# Github Actions Environment CLI Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO_URL = "https://api.github.com/repos"

# ******************************************************************************** #
