FROM python:3.12-slim

LABEL maintainer="<rmarshall31@gmail.com>"

ENV AWS_DEFAULT_REGION us-east-1

WORKDIR /var/task

# to allow you to connect to the app locally
EXPOSE 8000

# a place to store your sqlite databases
RUN mkdir /tmp/db

# create a python virtual environment for the app
RUN python -m venv /root/ve

# upgrade pip
RUN . /root/ve/bin/activate && pip --no-cache-dir install --upgrade pip

# install the requirements to the virtual environment
COPY requirements.txt /tmp/
RUN . /root/ve/bin/activate && pip --no-cache-dir install --upgrade -r /tmp/requirements.txt

# bashrc settings
RUN echo 'export PS1="\[\e[36m\]sail_lanier-cloud-shell>\[\e[m\] "' >> /root/.bashrc
RUN echo 'export AWS_PROFILE=sail-lanier' >> /root/.bashrc
RUN echo 'source /root/ve/bin/activate' >> /root/.bashrc
RUN echo 'set -o vi' >> /root/.bashrc
RUN echo 'alias ls="ls --color=auto"' >> /root/.bashrc

CMD ["bash"]
