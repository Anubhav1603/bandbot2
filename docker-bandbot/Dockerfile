FROM ubuntu:20.04

RUN apt-get -qqy update && \
    apt-get -qqy install unzip git wget python3.8 python3.8-dev python3-pip fonts-noto-cjk

RUN DEBIAN_FRONTEND="noninteractive" apt-get -qqy install tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    hicolor-icon-theme \
    libcanberra-gtk* \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libpango1.0-0 \
    libpulse0 \
    libv4l-0 \
    fonts-symbola \
    --no-install-recommends && \
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -qqy && \
    apt-get install -qqy google-chrome-stable --no-install-recommends 

RUN CD_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    echo "Using chromedriver version: "$CD_VERSION && \
    wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CD_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /tmp/ && \
    rm /tmp/chromedriver_linux64.zip && \
    mv /tmp/chromedriver /usr/bin/chromedriver && \
    chmod 755 /usr/bin/chromedriver

ARG NO_CACHE_LINE=12

RUN git clone https://github.com/kohs100/bandbot2
WORKDIR /bandbot2

RUN apt-get purge --auto-remove -y curl git unzip 

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

ENV LC_ALL C.UTF-8
ENV FILETOKEN DEFAULT

ADD entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]