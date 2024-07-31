import os

from search_module import scheduler
from search_module.utils.database_utils import get_recently_updated_rows
from search_module.utils.elasticsearch_synchronisation import index_new_rows
from search_module.utils.logs import print_log

@scheduler.task('interval', id='index_elasticsearch_job',seconds= int(os.getenv("TASK_TIME")))
def index_elasticsearch():
    tables = os.getenv("TABLES").split(",")
    for table in tables:
        page = 1
        per_page = 10
        response = get_recently_updated_rows(table,page,per_page)
        
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
            response = get_recently_updated_rows(table,page,per_page)
            if("error" in response):
                err = response["error"]
                print_log(f"Job Failed {err}","e")
            response = response["rows"]        