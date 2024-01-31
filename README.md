# PDF Extract and Process

PDF Extract and Process (PEaP) is a tool to extract data from set of different pdf, and bring them into a standard format for reporting.

### Structure

```
peap
├── dev-env
│   └── Dockerfile [Dev env with required toolset need to develop this project]
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── __init__.py
│   ├── main.py
└── tests
    ├── __init__.py
    ├── resources
    │   └── test.pdf
    └── test_main.py

```

### Development environment

Development of this project requires several external APIs/CLIs, for example the AWS CLI and AWS SAM CLI. In order to keep your host free of project specific items a Docker container can be used.

Build an image using the Dockerfile `docker build -t peap ./dev-env`

#### Create a container

You can now create a container with an interactive shell with the `docker run` command, but you need decide how to configure AWS CLI. You have two choices:

1. Mount your host .aws directory into the container with the run command `docker run -it  -v .:/app -v ~/.aws:/root/.aws peap`
2. Run your container `docker run -it  -v .:/app`, which will drop you into the bash shell, and follow the aws credentials flow inside your container. [If the container is lost or delete you will need to go through this step again when you recreate the container.]

#### IDE

For the best experience using VSC and your dev container, install Dev Containers by Microsoft. Then navigate to the extension and connect to the running container.

This way your VSC should recognize the Python packages installed in your container, and you should have access to code completion, linting, and other IDE features.

[Sorry for all those using PyCharm or other IDEs - YMMV]

### Dependencies Management

Dependencies are managed by [Poetry](https://python-poetry.org/), which is installed into the Docker image via the Dockerfile.

Within the interactive shell you can run the poetry cmds needs for the project.

### Code Lint Format

[Ruff](https://github.com/astral-sh/ruff) is available in the Docker image for linting and formatting the code to a recognised standard.
