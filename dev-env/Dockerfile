FROM public.ecr.aws/sam/build-python3.9:latest

WORKDIR /app

# Update the package repository and install the package
RUN yum -y update && \
    yum -y install curl && \
    yum clean all

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -    

ENV PATH="${PATH}:/root/.local/bin"

# Copy custom shell script
COPY setup_bash.sh /usr/local/bin/

# Make the script executable
RUN chmod +x /usr/local/bin/setup_bash.sh

# Run the script to set up aliases
RUN /usr/local/bin/setup_bash.sh

CMD [ "/bin/bash" ]

