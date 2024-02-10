# PDF Extract and Process

PDF Extract and Process (PEaP) is a tool to extract data from set of different pdf, and bring them into a standard format for reporting.

### Structure

```
peap
│ [Project related files]
├── dev-env [Dev env container with required toolset need to develop this project]
├── src [Production code]
└── tests [Test code]

```

### Development environment

Development of this project requires several external APIs/CLIs, for example the AWS CLI and AWS SAM CLI. In order to keep your host free of project specific items a Docker container can be used.

Build an image using the Dockerfile `docker build -t peap ./dev-env`

#### Create a container

You can now create a container with an interactive shell with the `docker run` command, but you need decide how to configure AWS CLI. You have two choices:

1. Mount your host .aws directory into the container with the run command `docker run -it  -v .:/app -v ~/.aws:/root/.aws peap`
2. Run your container `docker run -it  -v .:/app`, which will drop you into the bash shell, and follow the aws credentials flow inside your container. [If the container is lost or delete you will need to go through this step again when you recreate the container.]

You can mount your ssh-keys and forward localhost:8000 to container.local:5000, which is the port the flask server runs on `docker run -it -v ~/.ssh/:/root/.ssh -v .:/app -p 8000:5000 peap`

#### IDE

_Currently this isn't available due to the base image from aws not having the requierd libstdc++.so and glibc installed - next best thing is start an interactive shell inside of the vsc project_

For the best experience using VSC and your dev container, install Dev Containers by Microsoft. Then navigate to the extension and connect to the running container.

This way your VSC should recognize the Python packages installed in your container, and you should have access to code completion, linting, and other IDE features.

[Sorry for all those using PyCharm or other IDEs - YMMV]

### Dependencies Management

Dependencies are managed by [Poetry](https://python-poetry.org/), which is installed into the Docker image via the Dockerfile.

Within the interactive shell you can run the poetry cmds needs for the project.

Remember to execute `poetry install` in the root when you first create the container. This will install the required packages. After which you can execute other poetry commands e.g. `poetry run python3 src/main.py`

### Code Lint Format

[Ruff](https://github.com/astral-sh/ruff) is available in the Docker image for linting and formatting the code to a recognised standard.

### Testing

This project is setup using [pytest](https://docs.pytest.org/) There is a separate folder branch for `tests`, which mirrors the `src` folder.

To run all tests from the command line `poetry run pytest`
