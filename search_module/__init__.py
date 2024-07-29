from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_apscheduler import APScheduler

from search_module.config import Config
from search_module.utils.elasticsearch_synchronisation import ingest_data_to_elasticsearch

import os

db = SQLAlchemy()
scheduler = APScheduler()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
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
        
        # Every period of time, we will captures the changes in the database, and index new documents
        from search_module.jobs.elasticsearch_index_job import index_elasticsearch
        scheduler.init_app(app)
        # scheduler.start()
    from search_module.main import main_namespace
    api.add_namespace(main_namespace)

    # # Import the routes later to prevent circular import ( one of many solutions ) 
    # from search_module.main.routes import test
    # app.register_blueprint(test)

    return app