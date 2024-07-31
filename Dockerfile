FROM python:3.10
EXPOSE 5000
RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt /home/app/
RUN pip install --no-cache-dir  -r requirements.txt
COPY . /home/app/
# RUN celery -A make_celery  worker --loglevel=INFO --pool=solo 
# RUN celery -A search_module  beat --loglevel=INFO -l debug
CMD ["python", "run.py"]
