from elasticsearch.helpers import bulk, BulkIndexError 
import os
from search_module.utils.elasticsearch_utils import create_client, database_name
from sqlalchemy.sql import text



def ingest_data_to_elasticsearch(db,batch_size=200):
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"},500
    
    tables = os.getenv("TABLES").split(",")
    for table_name in tables:
        index_name = database_name +"-"+table_name
        print(index_name)
        index_exists = es_client.indices.exists(index=index_name)
        if index_exists:pass
        else:
            index_data(db,index_name,table_name,batch_size)
        

def index_data(db,index_name,table_name,batch_size):
    
    count_query = text(f'SELECT COUNT(*) FROM {table_name}') 
    total_rows = db.session.execute(count_query).scalar() 
    for start in range(0, total_rows, batch_size):
        if(start>=10000):break
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
                return {"error":"Could not connect to Elasticsearch!"},500
            bulk(es_client, data)
        except BulkIndexError as e:
            for error in e.errors:
                print("Error indexing document:", error)
            raise
    print(f"Data was successfully indexed into ElasticSearch : {index_name}")
        