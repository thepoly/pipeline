# Pipeline

Pipeline is [_The Rensselaer Polytechnic_](https://poly.rpi.edu)'s next
website. It will enable rapid development of new article layouts and
interactive features. In the long term, it will provide a solid platform for
our content over the coming decade and support _The Poly_'s focus on
online-first journalism.

## Requirements

Ensure these are installed before continuing.

- [Python 3.7](https://www.python.org) or Python 3.6
- [Pipenv](https://docs.pipenv.org)
- [npm](https://www.npmjs.com/get-npm)
- [Postgres](https://www.postgresql.org)

You can change Pipeline's settings to use SQLite instead of Postgres, but this is not recommended because Pipeline relies on Postgres's full-text search features.

## Getting started

Pipeline is written in Python. It uses Sass and PostCSS on the frontend with webpack to glue them together.

#### Note about Postgres

Pipeline expects to be able to connect to a Postgres database named `pipeline`. To set this up on macOS:

```
brew install postgresql
brew services start postgresql
createdb pipeline
```

### Installing

```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
npm install
npx wp --config webpack.development.config.js
pipenv install --dev
pipenv run python manage.py createcachetable
```

### Running

```
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If you have issues with the database, ensure that Postgres is running and you have created a database named `pipeline`.

#### Docker

Pipeline can also be run in its production configuration with Docker. It requires three containers: one for running the Django project with gunicorn, another to put nginx in front of it and additionally serve static files, and finally a Postgres container.

```docker-compose up```

Ensure that the `SECRET_KEY` environment variable is set. Additionally, run the following inside of the `django` container (e.g. `docker-compose exec django bash`):

```
python manage.py migrate
python manage.py createsuperuser
```

Pipeline will be available at port 8000 on localhost.

### Standards

Make sure you format your code with [Black](https://github.com/python/black) and use [Flake8](http://flake8.pycqa.org/en/latest/) to find problems.

## Status

Many of the following features are partially complete, but this isn't indicated. Talk to Sid if you need to know where something is right now.

- [ ] Articles
  - [x] Index pages
  - [ ] Article pages
    - [x] Basic layout
    - [ ] Section-specific layouts
    - [x] Editor previews
  - [x] Summaries
  - [x] Kickers
    - [x] Autocomplete
  - [x] Subdecks
  - [ ] Archive pages
  - [ ] WordPress importer
  - [ ] Old site importer
  - [x] Related to authors
- [ ] Photos
  - [x] Uploads
  - [x] Captions
  - [x] Bylines
  - [x] Multiple per article
  - [x] Galleries
- [ ] Syndication
  - [x] RSS feed
  - [x] Sitemap
  - [x] Facebook tags
  - [x] Twitter tags
  - [ ] oEmbed
  - [ ] Apple News
- [ ] Home page
  - [x] Basic article prioritization
  - [ ] Full user control of column layout
- [ ] Staff
  - [x] Index page
  - [ ] Individual pages
    - [x] Authored articles
    - [ ] Bylined photos
  - [x] Positions/terms
  - [x] Staff photos
- [ ] Contact
  - [x] Email addresses on staff pages
- [ ] Users
  - [x] Basic publish permission level
  - [x] Fine grained permissions
  - [ ] G Suite authentication
- [ ] Search
  - [x] Basic headline search
  - [x] Search all fields of articles
  - [ ] Search non-article pages
- [ ] Instrumentation
  - [x] Basic Prometheus metrics
  - [ ] DB metrics
  - [ ] HTTP Basic auth
