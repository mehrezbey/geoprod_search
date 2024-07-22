from flask_restx import Namespace

main_namespace = Namespace("main",description ="Query Documents in Elasticsearch")

import search_module.main.routes