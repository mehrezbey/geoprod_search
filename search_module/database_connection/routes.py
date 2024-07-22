from flask import request, jsonify
from flask_restx import  Resource
import os
from sqlalchemy.sql import text

from . import database_connection_namespace
from search_module import db

database_name = os.getenv("DATABASE_NAME")

@database_connection_namespace.route('/get', methods=["GET"])
class DatabaseResource(Resource):
    @database_connection_namespace.doc(params={'table':'Table name','page': 'Page number', 'per_page': 'Number of items per page'})
    def get(self):
        
        table = request.args.get('table')
        if(table is None): return {"Error":"Table name is mandatory"},400
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page
        try:
            sql_query = text(f'SELECT id FROM {table} LIMIT :limit OFFSET :offset') 
            result = db.session.execute(sql_query, {'limit': per_page, 'offset': offset})
            rows = [dict(row._mapping) for row in result]
            
            count_query = text(f'SELECT COUNT(*) FROM {table}') 
            total_count = db.session.execute(count_query).scalar()

            response = {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': (total_count + per_page - 1) // per_page,  
                'rows': rows
            }
            return jsonify(response)
        
        except Exception as e:
            return {'error': str(e)}, 500