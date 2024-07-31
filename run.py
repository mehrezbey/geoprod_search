from search_module import create_app

app = create_app()
# docker run -d --name elasticsearch -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xmx512m -Xms512m" -p 9200:9200 -p 9300:9300 docker.elastic.co/elasticsearch/elasticsearch:7.15.2
# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=mehrez -e RABBITMQ_DEFAULT_PASS=bey rabbitmq:3-management

if (__name__ == "__main__"):
    app.run(debug=True,use_reloader=False,host='0.0.0.0', port=5000)

# celery -A search_module  beat --loglevel=INFO -l debug
# celery -A make_celery  worker --loglevel=INFO --pool=solo 
