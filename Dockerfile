FROM python:3.10

WORKDIR /usr/src/app

RUN pip install celery[redis]==5.2.7
RUN pip install requests
RUN pip install BeautifulSoup4

COPY celery_config.py .
COPY calls.py .
COPY crawler.py .
