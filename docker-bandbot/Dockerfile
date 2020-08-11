FROM ubuntu:20.04

RUN apt-get -y update && \
    apt-get -y install git wget python3.8 python3.8-dev python3-pip fonts-noto-cjk

ARG CHROME_DRIVER_VERSION="latest"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install \
    ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN CD_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
  && echo "Using chromedriver version: "$CD_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CD_VERSION/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /tmp/ \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /tmp/chromedriver /usr/bin/chromedriver \
  && chmod 755 /usr/bin/chromedriver

RUN git clone https://github.com/kohs100/bandbot2
WORKDIR /bandbot2

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

ENV FILETOKEN DEFAULT

CMD ["/bandbot2/entrypoint.sh"]