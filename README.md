# Pipeline [<img align="right" width="200px" src="https://cloud.githubusercontent.com/assets/335234/18211402/6fb5bdd6-710b-11e6-93dc-f47559d8ba19.png">](https://poly.rpi.edu)
Pipeline is a tool for organizing, tracking, and distributing content for *The Rensselaer Polytechnic* or a similar newspaper.

## Goals

### Organization
Pipeline tracks an article from start to finish. As soon as an idea is proposed, it can be entered into Pipeline by an editor. Reporters and photographers can be assigned, and details about the article—such as event location and time, people to contact, and related tasks—can be recorded.

### Tracking
As an article is written, goes through copy, and is eventually published, a history of edits is recorded. Copy readers can easily see where articles are in the copy queue and advance them as they are edited.

### Distributing
After an article has been copy read, it can be pulled into Adobe InDesign for layout and published on a website. The website is simply a collection of static files for ease of deployment. As changes are made to articles, the website is automatically kept in-sync.

## Motivation

Currently, by the time an article is published, it exists in three separate places: Google Drive, our InDesign layout file, and the website. There is no single, authoritative history of edits. Additionally, organization of an issue's content is currently done with a spreadsheet, and it is not associated with the resulting articles.

## Running Pipeline

Pipeline's API is written in Python, and it uses Angular and TypeScript on the
frontend. To run it for development, not production, use these commands:

### API

```
pip install -r requirements.txt
gunicorn pipeline.api.api:api --reload -k gevent
```

### Frontend

```
cd web
npm install
npm start
```

### Editor

Requires Redis to be running on its default port. Additionally, the files in pipeline/editor should be served over HTTP (can be accomplished with `python -m http.server`).

```
pip install -r requirements.txt
cd pipeline/editor
python ws.py
```
