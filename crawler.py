import os
import requests
from bs4 import BeautifulSoup
from celery import Celery, chain
from time import sleep

os.environ.setdefault('CELERY_CONFIG_MODULE', 'celery_config')
app = Celery('calls')
app.config_from_envvar('CELERY_CONFIG_MODULE')

# app = Celery(
#     'tasks', broker=f'redis://{os.getenv("REDIS_USER")}:{os.getenv("REDIS_PASSWORD")}@{os.getenv("BROKER_HOST")}:6379/0')


@app.task(name='crawl')
def crawl(url, selector):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    for i in range(10):
        print(f'Wait... {i}')
        sleep(1)
    return soup.select(selector)


@app.task(name='extract')
def extract_info(data_items, selectors):
    result = []
    for item in data_items:
        doc = {}
        for k, v in selectors.items():
            tag = item.select(v['path'])
            if len(tag) > 0:
                if v['attr'] == 'text':
                    doc[k] = tag[0].text
                else:
                    doc[k] = tag[0][v['attr']]

        result.append(doc)
    return result
