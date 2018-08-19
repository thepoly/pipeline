# Pipeline

Pipeline is [_The Rensselaer Polytechnic_](https://poly.rpi.edu)'s next
website. It will enable rapid development of new article layouts and
interactive features. In the long term, it will provide a solid platform for
our content over the coming decade and support _The Poly_'s focus on
online-first journalism.

## Requirements

Ensure these are installed before continuing.

- [Python 3.7](https://www.python.org)
- [Pipenv](https://docs.pipenv.org)
- [npm](https://www.npmjs.com/get-npm)

### Optional

- [Postgres](https://www.postgresql.org)

By default, Django will use SQLite, which comes with Python. Postgres will be required once search gets more attention.

## Getting started

Pipeline is written in Python. It uses Sass and PostCSS on the frontend with webpack to glue them together. To
run Pipeline for development:

### Installing

```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
pipenv install
npm install
npx wp --config webpack.development.config.js
```

### Running

```
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Developing

Make sure you format your code with [Black](https://github.com/ambv/black) and use [Flake8](http://flake8.pycqa.org/en/latest/) to find problems. Compliance will soon be enforced on push.

## Status

Many of the following features are partially complete, but this isn't indicated. Talk to Sid if you need to know where something is right now.

- [ ] Articles
  - [x] Index pages
  - [ ] Article pages
    - [x] Basic layout
    - [ ] Section-specific layouts
    - [x] Editor previews
  - [x] Summaries
  - [ ] Kickers
    - [ ] Autocomplete
  - [ ] Subdecks
  - [ ] Archive pages
  - [ ] WordPress importer
  - [ ] Old site importer
  - [x] Related to authors
- [ ] Photos
  - [x] Uploads
  - [ ] Captions
  - [ ] Bylines
  - [x] Multiple per article
  - [ ] Galleries
- [ ] Syndication
  - [ ] RSS/atom feeds
  - [ ] Sitemap
  - [ ] Facebook tags
  - [ ] Twitter tags
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
  - [ ] Fine grained permissions
  - [ ] Google Apps authentication
- [ ] Search
  - [x] Basic headline search
  - [ ] Search all fields of articles
- [ ] Instrumentation
  - [x] Basic Prometheus metrics
  - [ ] DB metrics
  - [ ] HTTP Basic auth
