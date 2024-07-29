from elasticsearch import Elasticsearch, NotFoundError

import os

database_name = os.getenv("DATABASE_NAME")

def create_client():
    es_client = Elasticsearch(
        hosts=[{"host": "localhost", "port": 9200,"scheme": "http"}],
        timeout=30,
        max_retries=10, 
        retry_on_timeout=True 
    )
    return es_client
    

def extract_search_results(response):
    to_return = {}
    to_return["total"] =0
    to_return["hits"] = []
    if 'hits' in response and 'hits' in response['hits'] and 'total' in response['hits']:
        documents = response['hits']['hits']
        to_return["total"] = int(response["hits"]["total"]["value"])
        hits = []
        for hit in documents:
            source = hit.get('_source', {})
            hits.append(source)
        to_return["hits"] = hits

    return to_return

def query_index(index, query, fields , page, per_page ):
    """
        index : name of the index ( database_name-table_name) ( _all : to search in all indices)
        query : the text to search ( empty string will returns all documents )
        fields : one or multiple fields seperated by a comma , ( if it is empty, We will search in all fields)
    """
    es_client = create_client()
    if not es_client.ping():
        return {"error":"Could not connect to Elasticsearch!"}
    try:
        result = es_client.search(
            index = index,
            body={'query':{
                        "query_string": {
                            "query": "*"+query+"*",
                            'fields': fields
                            }
                        },
                        'from': (page - 1) * per_page,
                        'size': per_page
                    }
        )
        return extract_search_results(result), 200
    
    except NotFoundError:
        return {"error":"Index not found!"}, 404

    except Exception as e:
        return {"error":"An unexpected error occurred: " + str(e)},500
