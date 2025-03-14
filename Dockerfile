FROM python:3.12-slim

ENV AWS_DEFAULT_REGION=us-east-1

WORKDIR /var/task

EXPOSE 8000

RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && mkdir -p /tmp/db \
    && python -m venv /root/ve \
    && . /root/ve/bin/activate && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/

RUN . /root/ve/bin/activate && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

RUN echo 'export PS1="\[\e[36m\]sail_lanier-cloud-shell>\[\e[m\] "' >> /root/.bashrc && \
    echo 'export AWS_PROFILE=sail-lanier' >> /root/.bashrc && \
    echo 'source /root/ve/bin/activate' >> /root/.bashrc && \
    echo 'set -o vi' >> /root/.bashrc && \
    echo 'alias ls="ls --color=auto"' >> /root/.bashrc

CMD ["bash"]
