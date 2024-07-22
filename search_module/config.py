import os
from dotenv import load_dotenv

load_dotenv()

class Config : 
    SECRET_KEY= os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')+os.getenv("DATABASE_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS= False