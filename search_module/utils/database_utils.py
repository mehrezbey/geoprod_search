from sqlalchemy.sql import text

from search_module import db, scheduler
import os

# For the APscheduler ( it needs the context )
def get_recently_updated_rows(table, page, per_page):
    
    offset = (page - 1) * per_page
    interval = os.getenv("DATABASE_INTERVAL")
    column_update= os.getenv("COLUMN_UPDATE_NAME")
    with scheduler.app.app_context():
        try:
            sql_query = text(f'SELECT * FROM {table} WHERE {column_update} >= NOW() - INTERVAL {interval}  LIMIT :limit OFFSET :offset') 
            result = db.session.execute(sql_query, {'limit': per_page, 'offset': offset})
            rows = [dict(row._mapping) for row in result]
            count_query = text(f'SELECT COUNT(*) FROM {table} WHERE {column_update} >= NOW() - INTERVAL {interval}') 
            total_count = db.session.execute(count_query).scalar()

            response = {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': (total_count + per_page - 1) // per_page,  
                'rows': rows
            }
            return response
        
        except Exception as e:
            return {'error': str(e)}

#  For celery (similar to the previous one but it doesn't need contexte)
def get_recently_updated_rows_celery(table, page, per_page):
    
    offset = (page - 1) * per_page
    interval = os.getenv("DATABASE_INTERVAL")
    column_update= os.getenv("COLUMN_UPDATE_NAME")
    try:
        sql_query = text(f'SELECT * FROM {table} WHERE {column_update} >= NOW() - INTERVAL {interval}  LIMIT :limit OFFSET :offset') 
        result = db.session.execute(sql_query, {'limit': per_page, 'offset': offset})
        rows = [dict(row._mapping) for row in result]
        count_query = text(f'SELECT COUNT(*) FROM {table} WHERE {column_update} >= NOW() - INTERVAL {interval}') 
        total_count = db.session.execute(count_query).scalar()

        response = {
            'page': page,
            'per_page': per_page,
            'total': total_count,
            'pages': (total_count + per_page - 1) // per_page,  
            'rows': rows
        }
        return response
    
    except Exception as e:
        return {'error': str(e)}