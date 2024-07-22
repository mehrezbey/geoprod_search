from flask import request, jsonify
from flask_restx import Resource
import os

from search_module.utils.elasticsearch_utils import query_index
from . import main_namespace

database_name = os.getenv("DATABASE_NAME")


@main_namespace.route('/search', methods=["GET"])
class Search(Resource):
    @main_namespace.doc(params={
        'table':"The name of the table. Write '_all' if you want the search to include all tables.",
        'query':"The text to search. If you want to return all documents, do not write anything.",
        'fields':"The fields of the query seperated by ','. If you want to include all the fields do not write anything.",
        'page': 'The number of the page starting from 1. The default value = 1',
        'per_page': 'The number of documents in each page. The default value = 5'
        })
    def get(self):
        req = request.args
        if(not ("table" in req)):
            return jsonify(message="Error! Table name is mandatory!"), 405
        if(req["table"] !="_all"):
            index = database_name+"-"+ req["table"]
        else: 
            index = req["table"]
        if("query" in req):
            query = req["query"]
        else:
            query=""
        if("fields" in req):
            fields = req["fields"]
        else:
            fields=''
        if(fields==''):
            fields = ['*']
        else:
            fields = fields.split(",")
        if("page" in req):
            page = int(req["page"])
        else:
            page=1
        if("per_page" in req):
            per_page = int(req["per_page"])
        else:
            per_page=5
        return query_index(index,query,fields,page,per_page)

