import time
from stackapi import StackAPI
from celery import Celery

BACKEND_URL = 'redis://localhost:6379'
BROKER_URL = 'amqp://localhost'
celery_app = Celery('Crawler', broker=BROKER_URL, backend=BACKEND_URL)

KEY = '1e*14UFc3n18Nf9CPoLzDQ(('
SITE = StackAPI('stackoverflow', key=KEY)
SITE.page_size = 100


@celery_app.task(trail=True)
def _crawlSAPI(tag, start, end, sort='votes', order='desc'):
    QUESTIONS = []
    for i in range(start, end + 1):
        try:
            current = SITE.fetch('questions', tagged=tag,
                                 sort=sort, order=order, page=i)
            print(current['quota_remaining'])
            for x in current['items']:
                QUESTIONS.append((x['title'], x['link']))
            print('Crawled Page No. {}'.format(i))
        except:
            print('Error in Fetching Page Number ' + str(i))
            continue
    return QUESTIONS
