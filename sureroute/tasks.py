from celery import Celery
import requests
import datetime
import sqlalchemy
from .models import SureRoute, SureRouteResult, DBSession, Base
import transaction
from celery.signals import worker_init


@worker_init.connect
def bootstrap_pyramid(signal, sender):
    import os
    from pyramid.paster import bootstrap
    sender.app.settings = \
        bootstrap(os.environ['YOUR_CONFIG'])['registry'].settings
    print(sender.app.settings)
    engine = sqlalchemy.create_engine(sender.app.settings['sqlalchemy.url'])
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

app = Celery('tasks', broker='redis://localhost:6379/0',)


@app.task
def test_sureroute():
    for sureroute in DBSession.query(SureRoute).all():
        check_object.delay(sureroute)


@app.task
def check_object(sureroute):
    status_code = None
    try:
        status_code = requests.get(sureroute.object_path).status_code
    except:
        status_code = None
    result = SureRouteResult(sureroute_id=sureroute.id, time=datetime.datetime.now(), success=(status_code and status_code == 200),
                                 status_code=status_code)
    with transaction.manager:
        DBSession.add(result)
    DBSession.flush()
    print(DBSession.query(SureRouteResult).all())


@app.task
def crawl_website():
    return ''
