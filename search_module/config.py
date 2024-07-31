import os
from dotenv import load_dotenv

load_dotenv()

class Config : 
    SECRET_KEY= os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')+os.getenv("DATABASE_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SCHEDULER_API_ENABLED = True
    # CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    # CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
