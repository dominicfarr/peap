FROM public.ecr.aws/sam/build-python3.9:latest

WORKDIR /app

# Update the package repository and install the package
RUN yum -y update && \
    yum -y install curl && \
    yum clean all

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -    

ENV PATH="${PATH}:/root/.local/bin"

CMD [ "/bin/bash" ]

