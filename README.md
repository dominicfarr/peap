# PDF Extract and Process

PDF Extract and Process (PEaP) is a tool to extract data from set of different pdf, and bring them into a standard format for reporting.

### Structure

```
project
    ├── config.json [do not commit]
    ├── dev-env
    │   └── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── src
    │   └── main.py
    └── test
        └── resources
            └── test.pdf
    
```

### Development environment

Development of this project requires several external APIs/CLIs, for example the AWS CLI and AWS SAM CLI. In order to keep your host free of project specific items a docker container can be used.

Build an image `docker build -t peap ./dev-env` and then interact with your new container, mounting a volume to this project. `docker run -it  -v .:/app peap`

**_Before you run these commands you must first decide how your aws credentials should work._**

#### Configure AWS CLI

You have two choices.

1. Mount your host .aws file into the container with the run command `docker run -it  -v .:/app -v ~/.aws:/root/.aws peap`
2. Follow the aws credentials flow inside your container. [This method is more separate, but if the container is lost or delete you will need to go through this step again when you recreate the container]

#### IDE

For the best experience using VSC and your dev container, install Dev Containers by Microsoft. Then navigate to the extension and connect to the running container. 

This way your VSC should recognize the Python packages installed in your container, and you should have access to code completion, linting, and other IDE features.

[Sorry for all those using PyCharm or other IDEs - YMMV]


