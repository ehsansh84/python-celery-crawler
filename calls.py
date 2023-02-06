from celery import Celery, chain
app = Celery('calls')

urls = [
    'https://www.brainyquote.com/topics/motivational-quotes'
]

selectors = {
    'text': {
        'path': '.b-qt > div',
        'attr': 'text'
    },
    'author': {
        'path': '.bq-aut',
        'attr': 'text'
    },
    'author_url': {
        'path': '.bq-aut',
        'attr': 'href'
    }
}



chain(
    app.signature("crawl_task", args=[urls[0], 'div.quote']).set(queue="crawler"),
    app.signature("extract_task", args=[selectors]).set(queue="extract")
).apply_async()

