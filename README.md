# celery_task
Simple rest api using flask sqlalchemy celery

to start using you should install:
  pip install -r requirements.txt
  install RabbitMQ (in Ubuntu: sudo apt install rabbitmq-server)
  
starting use:
  check that rabbitmq working (in Ubuntu: sudo service rabbitmq-server status)
  start webserver: python run.py
  start Distributed Task Queue: celery -A run.celery_ worker --loglevel=info

Now you can send requests for your server by curl.

Some examples:
curl -i -H "Content-Type: application/json" -X POST -d '{"x":2, "y":5}' http://localhost:5000/api/pow
curl -i -H "Content-Type: application/json" -X POST -d '{"x":2, "y":5}' http://localhost:5000/api/add
curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/report

api methods:
POST - add, mul, div, pow
  http://localhost:5000/api/<method_name>
GET - report
  http://localhost:5000/api/report
