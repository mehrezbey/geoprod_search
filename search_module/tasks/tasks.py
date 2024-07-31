from search_module.utils.database_utils import get_recently_updated_rows_celery
from search_module.utils.elasticsearch_synchronisation import index_new_rows
from search_module.utils.logs import print_log

from flask import current_app
from celery import current_app as celery_app

import os

@celery_app.task
def periodic_task():
    # return "IT WORKS ! "
    with current_app.app_context():
        tables = os.getenv("TABLES").split(",")
        for table in tables:
            page = 1
            per_page = 10
            response = get_recently_updated_rows_celery(table,page,per_page)
            
            if("error" in response):
                err = response["error"]
                print_log(f"Job Failed {err}","e")
            response = response["rows"]
            if not response:
                print_log(f"Nothing new in the table {table}. No need to index anything.","w")
            else:
                print_log(f"Something has changed in  {table}. We will index the changes.","i")

            while response :
                index_new_rows(table, response)
                page+=1
                response = get_recently_updated_rows_celery(table,page,per_page)
                if("error" in response):
                    err = response["error"]
                    print_log(f"Job Failed {err}","e")

                response = response["rows"]


# celery -A search_module  beat --loglevel=INFO -l debug
# celery -A search_module  worker --loglevel=INFO --pool=solo

