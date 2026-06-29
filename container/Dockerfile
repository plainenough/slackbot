FROM python:3.12-slim-bookworm

WORKDIR /opt/slackbot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/slackbot

RUN useradd --create-home --shell /usr/sbin/nologin slackbot && \
    mkdir -p /opt/slackbot/data && \
    chown -R slackbot:slackbot /opt/slackbot

USER slackbot

VOLUME /opt/slackbot/data

ENV SLACKBOT_CONFIG=/opt/slackbot/data/config.yaml

CMD ["python3", "main.py"]

LABEL org.opencontainers.image.title="Slackbot"
LABEL org.opencontainers.image.description="Python Slack bot with Socket Mode"
LABEL org.opencontainers.image.source="https://github.com/plainenough/slackbot"
