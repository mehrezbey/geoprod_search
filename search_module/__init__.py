from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_apscheduler import APScheduler
from celery import current_app as celery_app
from datetime import timedelta

from search_module.config import Config
from search_module.utils.elasticsearch_synchronisation import ingest_data_to_elasticsearch
from search_module.utils.celery_utils import celery_init_app
import os


db = SQLAlchemy()
scheduler = APScheduler()

# For the celery tasks ( Or u can use the celery_app.conf.beat_schedule )
from search_module.tasks.tasks import periodic_task 
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(int(os.getenv("TASK_TIME")), periodic_task, name='periodic_task')
    sender.add_periodic_task(timedelta(seconds=int(os.getenv("TASK_TIME"))), periodic_task, name='periodic_task')


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    # For Celery
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.getenv("CELERY_BROKER_URL"),
            result_backend=os.getenv("CELERY_RESULT_BACKEND"),
            timezone='UTC'
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    # For swagger ( search api)
    api=Api(app,
        title="Geoprod Search Module",
        description="REST APIs",
        doc='/',
        version = "1.0"
    )
    with app.app_context():
        db.init_app(app)

        # In case you will run the script for the first time, it will upload the specific tables into elasticsearch
        ingest_data_to_elasticsearch(db)
        # Every period of time, we will captures the changes in the database, and index new documents( same as celery )
        from search_module.jobs.elasticsearch_index_job import index_elasticsearch
        scheduler.init_app(app)
        # scheduler.start()
    from search_module.main import main_namespace
    api.add_namespace(main_namespace)
    
    return app