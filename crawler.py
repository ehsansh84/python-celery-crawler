import os
import requests
from bs4 import BeautifulSoup
from celery import Celery

os.environ.setdefault('CELERY_CONFIG_MODULE', 'celery_config')
app = Celery('tasks')
app.config_from_envvar('CELERY_CONFIG_MODULE')


app.conf.task_routes = {'app.tasks.crawl_task': {'queue': 'crawler'},
                        'app.tasks.extract_task': {'queue': 'extract'}
                        }


@app.task(name='crawl_task')
def crawl(url, selector):
    try:
        result = requests.get(url, verify=False)
        soup = BeautifulSoup(result.text, 'html.parser')
        return soup.select(selector)
    except Exception as e:
        print(str(e))


@app.task(name='extract_task')
def extract_info(data_items, selectors):
    result = []
    if data_items is None:
        print('No data received!')
    else:
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
