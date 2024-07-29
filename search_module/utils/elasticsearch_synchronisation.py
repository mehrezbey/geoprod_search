from elasticsearch.helpers import bulk, BulkIndexError 
from sqlalchemy.sql import text
import os

from search_module.utils.elasticsearch_utils import create_client, database_name
from search_module.utils.logs import print_log

def index_data(db,index_name,table_name,batch_size):
    
    # First, we create the index.
    # Define dynamic template mapping
    mapping = {
        "mappings": {
            "dynamic_templates": [
                {
                    "all_fields_as_text": {
                        "match_mapping_type": "*",
                        "mapping": {
                            "type": "text"
                        }
                    }
                }
            ]
        }
    }
    es_client = create_client()
    if not es_client.ping():
        print_log("Could not connect to Elasticsearch while creating the index!","e")
        return   
    es_client.indices.create(index=index_name, body=mapping)
    count_query = text(f'SELECT COUNT(*) FROM {table_name}') 
    total_rows = db.session.execute(count_query).scalar() 
    for start in range(0, total_rows, batch_size):
        sql_query = text(f'SELECT * FROM {table_name} LIMIT :limit OFFSET :offset') 
        result = db.session.execute(sql_query, {'limit': batch_size, 'offset': start})
        rows = [dict(row._mapping) for row in result]
        data = [
            {
                '_index': index_name,
                '_id': row.get('id'),
                '_source': row
            }
            for row in rows
        ]
        try:
            es_client = create_client()
            if not es_client.ping():
                print_log("Could not connect to Elasticsearch while ingesting data to Elasticsearch !","e")
                return
            bulk(es_client, data)
        except BulkIndexError as e:
            for error in e.errors:
                print_log(f"Error indexing document: {error}","e" )
            raise
    return {"message": f"Data was successfully indexed into ElasticSearch : {index_name}"}
    
def ingest_data_to_elasticsearch(db,batch_size=50):
    es_client = create_client()
    if not es_client.ping():
        print_log("Could not connect to Elasticsearch while ingesting data to Elasticsearch !","e")
        return
    tables = os.getenv("TABLES").split(",")
    for table_name in tables:
        index_name = database_name +"-"+table_name
        index_exists = es_client.indices.exists(index=index_name)
        if index_exists:
            print_log(f"{index_name} already exists! No need to index all the rows of the table {table_name}","i")
        else:
            print_log(f"{index_name} doesn't exist! We need to index all the rows of the table {table_name}","i")
            res = index_data(db,index_name,table_name,batch_size)
            if("message"in res):
                print_log(res["message"],"s")
                total = es_client.count(index=index_name)['count']
                print_log(f"{total} documents were indexd into {index_name}.","s")

def index_new_rows(table, rows):
    
    index_name = os.getenv("DATABASE_NAME") + "-" + table
    indices = [
            {
                '_index': index_name,
                '_id': row.get('id'),
                '_source': row
            }
            for row in rows
        ]
    try:
        es_client = create_client()
        if not es_client.ping():
            print_log("Could not connect to Elasticsearch while indexing the new rows to Elasticsearch !","e")
            return
        bulk(es_client, indices)
    except BulkIndexError as e:
        for error in e.errors:
            print_log(f"Error indexing document: {error}","e" )
        raise
    return {"message": f"Data was successfully indexed into ElasticSearch : {index_name}"}