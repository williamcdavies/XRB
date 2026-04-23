FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        rsync \
        openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/sshd

WORKDIR /app

COPY server/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY server/ /app/

COPY rsync/sshd_config         /etc/ssh/sshd_config
COPY rsync/xrb-rsync-wrapper   /usr/local/bin/xrb-rsync-wrapper
COPY rsync/entrypoint.sh       /rsync-entrypoint.sh
RUN chmod +x /usr/local/bin/xrb-rsync-wrapper /rsync-entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/rsync-entrypoint.sh"]
