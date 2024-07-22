from flask_restx import Namespace

database_connection_namespace = Namespace("Database Connection",description ="Select rows from database")

import search_module.database_connection.routes