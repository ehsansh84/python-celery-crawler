import os
import requests
from bs4 import BeautifulSoup
from celery import Celery, chain
from time import sleep

os.environ.setdefault('CELERY_CONFIG_MODULE', 'celery_config')
app = Celery('tasks')
app.config_from_envvar('CELERY_CONFIG_MODULE')

# app = Celery(
#     'tasks', broker=f'redis://{os.getenv("REDIS_USER")}:{os.getenv("REDIS_PASSWORD")}@{os.getenv("BROKER_HOST")}:6379/0')


app.conf.task_routes = {'app.tasks.crawl_task': {'queue': 'crawler'},
                        'app.tasks.extract_task': {'queue': 'extract'}
                        }


@app.task(name='crawl_task')
def crawl(url, selector):
    try:
        print(url)
        result = requests.get(url)
        print(result.status_code)
        soup = BeautifulSoup(result.text, 'html.parser')
        print('DOOOOONE!')
        return soup.select(selector)
    except Exception as e:
        print(str(e))


@app.task(name='extract_task')
def extract_info(data_items, selectors):
    print('SSSS')
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
