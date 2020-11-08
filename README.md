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

Pipeline is written in Python. It uses Sass and PostCSS on the frontend with webpack to glue them together. For new users working within a virtual machine, it is strongly recommended to use Ubuntu. 

#### Note about Postgres

Pipeline expects to be able to connect to a Postgres database named `pipeline`. To set this up on macOS:

```
brew install postgresql
brew services start postgresql
createdb pipeline
```

To setup Postgres on [Arch Linux](https://www.archlinux.org/):

```
sudo pacman -Syu # Optional, to refresh and update packages
sudo pacman -S postgresql
sudo -u postgres initdb --locale en_US.UTF-8 -D /var/lib/postgres/data
sudo systemctl start postgresql
```

To setup Postgres on [Ubuntu](https://ubuntu.com/):

```
// Install
sudo apt-get update
sudo apt-get -y install postgresql postgresql-contrib
// Setup
sudo -i -u postgres
psql
CREATE USER postgres WITH PASSWORD 'postgres'
\q
*reopen terminal*
sudo -u postgres psql
\password postgres // Enter 'postgres' twice
\q
*reopen terminal*
sudo systemctl start postgresql
```

The default dev database, defined in `settings/dev.py` uses the following postgres url: `postgresql://postgres:postgres@127.0.0.1:5432/pipeline` make sure that your database is configured to these settings. The pipeline database must exist, and the user `postgres` must exist with password `postgres`. Read more about postgres urls [here](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING).

Read about creating a user [here](https://www.postgresql.org/docs/10/role-attributes.html). You will probably want postgres to be a superuser.

### Installing

```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
npm install
npx webpack --config webpack.development.config.js
pipenv install --dev
pipenv run python manage.py createcachetable
```

On Ubuntu:
```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
sudo apt install npm
npx webpack --config webpack.development.config.js // Type "yes" when prompted
npm audit fix
sudo apt install pipenv
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

### How to make changes to styling

With your terminal/command prompt running ```python manage.py runserver```, open another at the project folder location and run ```npm run watch```.
Now you can edit styles at pipeline/pipeline/static/css/pipeline.scss

## Status

Many of the following features are partially complete, but this isn't indicated. Look at the Issues page if you need to know what is being worked on.

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
