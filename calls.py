from crawler import crawl, extract_info
from celery import Celery, chain
app = Celery('calls')

print('Starting...')
urls = [
    'https://quotes.toscrape.com',
]

selectors = {
    'text': {
        'path': 'span:nth-child(1)',
        'attr': 'text'
    },
    'author': {
        'path': '.author',
        'attr': 'text'
    },
    'author_url': {
        'path': 'span:nth-child(2)>a',
        'attr': 'href'
    }
}



chain(
    app.signature("crawl_task", args=[urls[0], 'div.quote']).set(queue="crawler"),
    app.signature("extract_task", args=[selectors]).set(queue="extract")
).apply_async()

# data = crawl(url=urls[0], selector='div.quote')
print('Done!')

# print(extract_info(data, selectors))
