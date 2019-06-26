FROM lambci/lambda:build-python3.6

LABEL maintainer="<rmarshall31@gmail.com>"

ENV AWS_DEFAULT_REGION us-east-1

WORKDIR /var/task

# to allow you to connect to the app locally
EXPOSE 8000

# a place to store your sqlite databases
RUN mkdir /tmp/db

# install yum packages
RUN yum install --releasever=latest -y vim

# create a python virtual environment for the app
RUN python -m venv /root/ve

# upgrade pip
RUN pip install --upgrade pip

# yum update
RUN yum makecache fast
RUN yum -y update

#set awsregion to us-east-1
RUN echo "us-east-1" > /etc/yum/vars/awsregion

# install the requirements to the virtual environment
COPY requirements.txt /tmp/
RUN source /root/ve/bin/activate && pip install -r /tmp/requirements.txt

# install the precompiled sqlite package for local testing
RUN tar -xzf /root/ve/lib/python3.6/site-packages/lambda_packages/sqlite3/python3.*-sqlite3-*.tar.gz -C /root/ve/lib/python3.6/site-packages/

# bashrc settings
RUN echo 'export PS1="\[\e[36m\]sail_lanier-cloud-shell>\[\e[m\] "' >> /root/.bashrc
RUN echo 'export AWS_PROFILE=sail-lanier' >> /root/.bashrc
RUN echo 'source /root/ve/bin/activate' >> /root/.bashrc
RUN echo 'set -o vi' >> /root/.bashrc
RUN echo 'alias ls="ls --color=auto"' >> /root/.bashrc
RUN echo 'alias vi="vim"' >> /root/.bashrc

CMD ["bash"]