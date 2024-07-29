from search_module import create_app

app = create_app()
# docker run -d --name elasticsearch -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xmx512m -Xms512m" -p 9200:9200 -p 9300:9300 docker.elastic.co/elasticsearch/elasticsearch:7.15.2
if (__name__ == "__main__"):
    app.run(debug=True,use_reloader=False)
