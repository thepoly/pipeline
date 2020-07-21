# Setting Up on a Windows environment

This is to hopefully clear any confusion that one may go through.

## My System Specs

```
OS Name Microsoft Windows 10 Education
Version 10.0.19041 Build 19041
Ubuntu
```

## Getting Started

At first, everything may seem really confusing and overwhelming. First, start off by
reading the Readme on the GitHub. It’s from the perspective of a Linux user and
expects some knowledge of the technologies.

Getting the right technologies is the first key part. Follow the links in the readme
and get NPM and Pipenv setup. One trouble you may encounter is conflicting versions
of Python. Make sure you are using Python3. To check use:

```
python --version
```

If it is Python 2, make sure you install Python 3. Afterwards, you can execute the
same commands but this time add "Python3 -m" infront of it. For example:

```
python3 -m pipenv --version
```

Now with NPM, Pipenv, and Python3 down, we have PostgreSql, “a free and open-source
relational database management system emphasizing extensibility and SQL compliance.”

A database basically handles all the data associated with the front-end.
You basically request and send data to the database. Setting this up may be confusing.
The instructions weren’t too clear for Windows Users. First download PostgreSql for
Windows and on Setup, make sure to make the user named "postgres" with password
"postgres". You can't do this later on. You must do this during setup. I setup SQL by
looking at section 1 of the [tutorial](https://www.postgresqltutorial.com/).

You can learn more as you need to. Only the first section is needed to set up. Once you've
made your server and a database named “pipeline” you’ll be able to actually run the web
app locally. This way you can see local changes you’ve made to the code.

First off, when cloning the project from git, directly clone it. Directly cloning it with
the “git clone” command is the way to go. Or you can use their command to do it. Note that
you must be a contributor to do it. Afterwards, you can install the dependencies. The
dependencies are basically modules that your code needs to work. By executing “npm install”
in the folder (the directory with the package.json file) you are installing all the
dependencies listed in the package.json file.

Do the following:

```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
npm install
npx webpack --config webpack.development.config.js
pipenv install --dev
pipenv run python manage.py createcachetable
```

You might not understand what these commands do right now, but you will when you get into
DJango more.

Now you run with:

```
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

This is how you run the webapp to see your local changes. If it fails, it most likely means
your database was set up incorrectly. Do note that the migrate command just makes sure
all the migrations are done. “Migrations are Django's way of propagating changes you make to
your models (adding a field, deleting a model, etc.) into your database schema. They're
designed to be mostly automatic, but you'll need to know when to make migrations, when to
run them, and the common problems you might run into.”