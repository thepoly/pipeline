FROM python:3.6

WORKDIR /app

ADD ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["pytest"]
