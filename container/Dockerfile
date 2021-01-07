# Base should be ubuntu 18
FROM ubuntu:bionic

# Some simple labels these just signify where it needs to go
LABEL     org.label-schema.name="Slackbot" \
          org.label-schema.description="Python-Bot for slack." \
          org.label-schema.url="https://github.com/plainenough/slackbot.git" \
          org.label-schema.vendor="Tosstalk.com" \
          org.label-schema.version=1.0.1

# Update the image
RUN apt-get update -yqq &&\
apt-get upgrade -yqq

# Install Python
RUN apt-get install -yqq python3 python3-pip

# Set Our Running Directory
WORKDIR /opt/slackbot/

# Copy all the code into the working directory
COPY . /opt/slackbot

# Volume
VOLUME /opt/slackbot/data

# Install python requirements
RUN pip3 install -r requirements.txt

# Finally run the code
CMD python3 main.py
