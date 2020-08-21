# Pipeline

Pipeline is [_The Rensselaer Polytechnic_](https://poly.rpi.edu)'s next
website. It will enable rapid development of new article layouts and
interactive features. In the long term, it will provide a solid platform for
our content over the coming decade and support _The Poly_'s focus on
online-first journalism.

## Section 1: Preface

The instructions provided in this document are based on the perspectives of a MacOS user. Nevertheless, the steps outlined here are important and should be similarly followed by every system.

Additional documentation can be found in the [documentation](https://github.com/thepoly/pipeline/tree/master/documentation) folder and the repository's [wiki](https://github.com/thepoly/pipeline/wiki). If you can't find what you're looking for within these resources, please don't hesitate to reach out to your mentor.

Document updated most recently for: MacOS Mojave 10.14.6

## Section 2: Requirements

Ensure these are installed before continuing. The provided links should help you with installation, 

- [Homebrew](https://brew.sh/)
  - If running `brew -v` in Terminal gives you a version number, you already have it installed.
- [Python 3.7](https://www.python.org) or Python 3.6
- [Pipenv](https://docs.pipenv.org)
- [npm](https://www.npmjs.com/get-npm)
- [Postgres](https://www.postgresql.org)
  - **Importantly, be sure to leave the default options checked. Your port number should default to '5432' and your user name and password should be set to 'postgres'.**

*You can change Pipeline's settings to use SQLite instead of Postgres, but this is not recommended because Pipeline relies on Postgres's full-text search features.*

## Section 3: Getting Started

*Pipeline is written in Python. It uses Sass and PostCSS on the frontend with webpack to glue them together.*

### Section 3.1: Note about Postgres

Pipeline expects to be able to connect to a Postgres database named `pipeline`. To set this up on macOS:

```
brew install postgresql
brew services start postgresql
createdb pipeline
```

#### Section 3.1.1: If you are asked for a password
After running `createdb pipeline`, you might be asked for a password for your desktop username. You'll find that your desktop password fails if this is the case. You'll need to switch your username to 'postgres'.

```
psql -U postgres
```

Enter 'postgres' as your password. The command 'psql' will open the postgres command line. To create the pipeline database from here, you'll need to do:

```
CREATE DATABASE pipeline;
```

Note the ';' (semicolon), this is required syntax for the end of a command in SQL.

To confirm the database has been created, you can run:

```
\l
```

This will show you a list of databases.

To exit this command line, enter:

```
\q
```

### Section 3.2: Installing

GitHub can be used through the command line or with its desktop interface, [GitHub Desktop](https://desktop.github.com/). Clone the repository into a folder on your local machine using the following command or do so through the Desktop app.

```
git clone git@github.com:thepoly/pipeline.git
```

Then do the following (make sure you are located in the cloned repository folder on your local machine):
```
cd pipeline
```

This next series of commands are important. If there are error messages here, try reading through the Terminal output, and troubleshoot your issues by looking them up online. If you need extra troubleshooting help, reach out to your mentor and potentially other members of your team.
```
npm install
npx webpack --config webpack.development.config.js
pipenv install --dev
pipenv run python manage.py createcachetable
```

### Section 3.3: Running for the First Time

```
pipenv shell
python manage.py migrate
python manage.py createsuperuser
```

After entering the last command, i.e., `...createsuperuser` enter a username, password, and email (optional). Follow the Terminal prompts closely and remember these credentials. This will be your **Wagtail Admin Login**.

```
python manage.py runserver
```

*If you have issues with the database, ensure that Postgres is running and you have created a database named `pipeline`.*

### Section 3.4: Viewing the Site for the First Time

Once the server is up and running with `python manage.py runserver`, you should be able to access your development environment in your browser.

Visit `localhost` at port `8000`. There are two ways to formally access this: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and [http://localhost:8000/](http://localhost:8000/). *Both mean the same thing, `localhost` and `127.0.0.1` are synonymous with each other. The `:8000` specifies the port number.*



## Section 4: 


## Section 5: Docker (Optional)

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
