FROM python:3.6

WORKDIR /app

ADD ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000
CMD ["gunicorn", "api:api", "--reload", "-k", "gevent", "-b", "0.0.0.0"]
