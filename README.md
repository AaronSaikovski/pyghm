<div align="center">

# PyGithubManager (pyghm)- v1.0.0

A simple python CLI tool to create github environments, add,remove and update secrets and variables for a given repository and environment.

</div>

## Software Requirements:

- [Python v3.13.x](https://www.python.org/) - or higher needs to be installed.
- [UV](https://github.com/astral-sh/uv) - UV Python pqckage management tool.
- [Taskfile](https://taskfile.dev/) - Modern makefile replacement to run the build chain commands listed below.
- [Bandit](https://github.com/PyCQA/bandit/) - Python security linter.

## Environment Setup:

You will need to provide your github PAT/Token in the format:

```bash
# for Linux/MacOS
export GITHUB_TOKEN="xxxxxxx"

# for Windows/Powershell
$env:GITHUB_TOKEN="xxxxxxx"
```

## Clone Repo:

```bash
git clone https://github.com/AaronSaikovski/pyghm
cd pyghm
```

## Installation:

The toolchain is driven by using [Taskfile](https://taskfile.dev/) and all commands are managed via the file `Taskfile.yml`

The list of commands is as follows:

```bash
* activate:           Activates the virtual environment.
* build:              uses uv build to package your Python application into a single package.
* clean:              Cleans the environment, Overwrites the pyproject.toml file.
* create:             Inits the python project using UV and creates and activates a new virtual environment.
* default:            Call Create as default cmd.
* deps:               Install the dependencies.
* dist:               Runs Pyinstaller to create a self-contained executable.
* docker-build:       builds a docker image based on the docker fil.e
* docker-run:         builds a docker image based on the docker file.
* lint:               Lints the project and performs type checking.
* reqs:               Lock dependencies declared in a pyproject.toml to requirements.txt.
* run:                Run the script main.py.
* seccheck:           Checks for vulnerabilities in the project.
* test:               Tests the project.
* update:             updates dependency versions.
```

Execute using the taskfile utility:

```bash
task <command_from_above_list>
```

To get started type:

- `task create` - this will create a new environment, fetch the dependencies and activate the virtual environment in one step.
- `task run` - to run project in the src folder.
- `task clean` - to delete everything - venv, deps etc.
- `task build` - to build a redistributable package.

## Execution:

```bash
# Ensure that the GITHUB_TOKEN has been set as an environment variable as above.

# The commands are:
* ./pyghm get-repo --repo USER/REPO -> To return information about a repository.
* ./pyghm create-env --repo USER/REPO --env ENV_NAME -> Create a new github environment.
* ./pyghm create-var --repo USER/REPO --env ENV_NAME --name MY_VAR --value "value" -> Create a new github environment variable.
* ./pyghm update-var --repo USER/REPO --env ENV_NAME --name MY_VAR --value "new-value" -> Updates a given github environment variable.
* ./pyghm delete-var --repo USER/REPO --env ENV_NAME --name MY_VAR -> Deletes a given github environment variable.
* ./pyghm check-var --repo USER/REPO --env ENV_NAME --name MY_VAR -> Checks if a given Github environment variable exists.
* ./pyghm list-vars --repo USER/REPO --env ENV_NAME -> Lists all the environment variables for a given repository.
* ./pyghm create-secret --repo USER/REPO --env ENV_NAME --name MY_SECRET --value "secret" -> Create a new github environment secret.
* ./pyghm update-secret --repo USER/REPO --env ENV_NAME --name MY_SECRET --value "new-secret" -> Updates a given github environment secret.
* ./pyghm delete-secret --repo USER/REPO --env ENV_NAME --name MY_SECRET -> Deletes a given github environment secret.

# ./pyghm will have to be substituted with the ./pyghm.exe on Windows.

# Where USER/REPO, ENV_NAME, MY_VAR, MY_SECRET and values are to be passed to the commands on the commandline.
```

