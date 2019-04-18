FROM node:10 as node

COPY . /app/
WORKDIR /app
RUN npm ci
RUN npx webpack-command --config webpack.production.config.js

FROM python:3.7 as python
LABEL maintainer="tech@poly.rpi.edu"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE pipeline.settings.production

RUN pip install pipenv
COPY ./Pipfile ./Pipfile.lock /app/
WORKDIR /app
RUN pipenv install --system --deploy

COPY . /app/
COPY --from=node /app/pipeline/static/webpack_bundles/ /app/pipeline/static/webpack_bundles/
COPY --from=node /app/webpack-stats.json /app/

COPY ./start.sh start.sh
EXPOSE 8000
CMD ["./start.sh"]
