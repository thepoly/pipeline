FROM node:10 as node

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npx webpack --config webpack.production.config.js --display errors-only

FROM python:3.7 as python
LABEL maintainer="tech@poly.rpi.edu"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE pipeline.settings.production

RUN groupadd -r pipeline && useradd --no-log-init -r -g pipeline pipeline

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
