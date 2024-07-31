# geoprod_search

To run the app : python run.py
To run the celery worker : celery -A make_celery  worker --loglevel=INFO --pool=solo 
To run the celery beats : celery -A search_module  beat --loglevel=INFO -l debug