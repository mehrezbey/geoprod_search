from search_module import create_app
from search_module.tasks.tasks import periodic_task 
flask_app = create_app()
celery_app = flask_app.extensions["celery"]