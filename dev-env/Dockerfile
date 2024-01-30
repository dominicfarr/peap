FROM public.ecr.aws/sam/build-python3.9:latest

COPY requirements.txt /app

WORKDIR /app

RUN python3 -m pip install --no-cache-dir --upgrade pip -r requirements.txt

# Update the package repository and install the package
RUN yum -y update && \
    yum -y install tree && \
    yum clean all

CMD [ "/bin/bash" ]

