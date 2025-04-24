FROM python:3.13.2-slim

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /booking/docker/app.sh

CMD bash -c "gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 & celery -A app.tasks.config:celery worker --loglevel=info & celery -A app.tasks.celer:celery flower --loglevel=info"
