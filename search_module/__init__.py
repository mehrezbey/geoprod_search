from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

from search_module.config import Config
from search_module.utils.elasticsearch_synchronisation import ingest_data_to_elasticsearch


db = SQLAlchemy()

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
        ingest_data_to_elasticsearch(db) # In case you will run the script for the first time, it will upload the database into elasticsearch

    from search_module.main import main_namespace
    api.add_namespace(main_namespace)

    from search_module.database_connection import database_connection_namespace
    api.add_namespace(database_connection_namespace)
    
    # # Import the routes later to prevent circular import ( one of many solutions ) 
    # from search_module.main.routes import test
    # app.register_blueprint(test)
    return app