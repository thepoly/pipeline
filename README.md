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
  - **Importantly, be sure to leave the default options checked. Your port number should default to `5432` and your user name and password should be set to `postgres`.**

*You can change Pipeline's settings to use SQLite instead of Postgres, but this is not recommended because Pipeline relies on Postgres's full-text search features.*

## Section 3: Getting Started

Pipeline is written in Python. It uses Sass and PostCSS on the frontend with webpack to glue them together.

### Section 3.1: Note about Postgres

Pipeline expects to be able to connect to a Postgres database named `pipeline`. To set this up on macOS:

```
brew install postgresql
brew services start postgresql
createdb pipeline
```

#### Section 3.1.1: If you are asked for a password
After running `createdb pipeline`, you might be asked for a password for your desktop username. You'll find that your desktop password fails if this is the case. You'll need to switch your username to `postgres`.

```
psql -U postgres
```

Enter `postgres` as your password. The command `psql` will open the postgres command line. To create the pipeline database from here, you'll need to do:

```
CREATE DATABASE pipeline;
```

Note the `;` (semicolon), this is required syntax for the end of a command in SQL.

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

This next series of commands are important. If there are error messages here, try reading through the Terminal output, and troubleshoot your issues by looking them up online. If you need extra troubleshooting help, reach out to your mentor and possibly other members of your team.
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

After entering the last command, i.e., `python manage.py createsuperuser` enter a username, password, and email (optional). Follow the Terminal prompts closely and remember these credentials. This will be your **Wagtail Admin Login**.

```
python manage.py runserver
```

*If you have issues with the database, ensure that Postgres is running and you have created a database named `pipeline`.*

### Section 3.4: Viewing the Site for the First Time

Once the server is up and running with `python manage.py runserver`, you should be able to access your development environment in your browser.

Visit `localhost` at port `8000`. You can access this by visiting [127.0.0.1:8000](http://127.0.0.1:8000/) or [localhost:8000](http://localhost:8000/). *Both mean the same thing, `localhost` and `127.0.0.1` are synonymous with each other. The `:8000` specifies the port number.*

When you visit the site, you should see the following message on a white screen: `Welcome to your new Wagtail site!`.

This is normal. You will now need to go the admin page of the site. Go to [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) or [localhost:8000/admin](http://localhost:8000/admin).

You'll need to use your new **Wagtail Admin Login** from the previous section to sign in. Once you do, you'll see the Wagtail interface on the screen. You can use the tabs on the left side of the screen or the url to navigate around this interface. *Wagtail allows both non-developers and developers add content to their Django site.*

Then, perform the following steps (you can find this sequence of steps on the wiki [here](https://github.com/thepoly/pipeline/wiki/Welcome-to-your-new-Wagtail-site!)).
1. Navigate to localhost:8000/admin/pages and delete the page there.
2. First, you have to create an article page that can go on your homepage. Click "add child page" and publish an article page.
3. Click "add child page," and create a home page. Call it "Home" and feature the article that you made on the page.
4. Publish the page.
5. Navigate to Settings > Sites. Click the "Add a site" in the top right corner. The hostname and port are whatever you set them to be (typically localhost and 80 respectively), and the root page should be the home page you just made.

As of yet, there is no easy way to immediately fill out your version of the Polytechnic site. You'll need to add your own test articles and pages manually. You can do this by copying over articles from the [Poly](https://poly.rpi.edu) site onto your development environment.

## Section 4: Now... How to Start and Stop 
Now, whenever you need to start up the server, you'll need to do the following.

Open the `pipenv` shell, start your database, and run your server.
```
pipenv shell
brew services start postgresql
python manage.py runserver
```

Then, once you're ready to stop the server, enter control-C (the `control` and `C` keys on your keyboard). Then stop the database, and exit the shell.
```
brew services stop postgresql
exit
```

That's all there is to it! The only other thing to remember is that you'll need to use the [admin](http://localhost:8000/admin) page of the site to manage the content of your development environment!

## Section 5: Additional (Less Important) Sections
### Section 5.1: Docker (Optional)

Pipeline can also be run in its production configuration with Docker. It requires three containers: one for running the Django project with gunicorn, another to put nginx in front of it and additionally serve static files, and finally a Postgres container.

```docker-compose up```

Ensure that the `SECRET_KEY` environment variable is set. Additionally, run the following inside of the `django` container (e.g. `docker-compose exec django bash`):

```
python manage.py migrate
python manage.py createsuperuser
```

Pipeline will be available at port 8000 on localhost.

### Section 5.2: Standards

The [issues](https://github.com/thepoly/pipeline/issues) page has features we'd like to implement and bugs we'd like to address.

Typical workflow for this project means a new branch should be created for each new feature being developed.

Make sure you format your code with [Black](https://github.com/python/black) and use [Flake8](http://flake8.pycqa.org/en/latest/) to find problems.

### Section 5.3: How to make changes to styling

With your terminal/command prompt running `python manage.py runserver`, open another at the project folder location and run `npm run watch`.
Now you can edit styles at pipeline/pipeline/static/css/pipeline.scss
