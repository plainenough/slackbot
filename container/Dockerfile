FROM ubuntu:bionic
RUN apt update &&\
apt upgrade -y
RUN apt install -y python3 python3-pip
RUN pip3 install slackclient \
pyyaml \
WORKDIR /opt/slackbot/
COPY . /opt/slackbot
CMD python3 main.py && tail -f /opt/slackbot/data/slackbot.log
LABEL     org.label-schema.name="Slackbot" \
          org.label-schema.description="Python-Bot for slack." \
          org.label-schema.url="https://github.com/plainenough/slackbot.git" \
          org.label-schema.vendor="Tosstalk.com" \
          org.label-schema.version=$version
