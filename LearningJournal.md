# Learning Journal

This journal is to document my experience as a complete beginner to front-end as a
Windows User.

## My System Specs

```
OS Name Microsoft Windows 10 Education
Version 10.0.19041 Build 19041
Ubuntu
```

## Getting Started

At first, everything may seem really confusing and overwhelming. First, start off by
reading the Readme on the GitHub. It’s not the best as it’s from the perspective of
a Linux user and expects some knowledge of the technologies.

Getting the right technologies is the first key part. The readme should be enough for
you to get NPM and Pipenv setup. One trouble I did have was from conflicting versions
of Python. When I downloaded Python3, it conflicted with my Python 2, thus when I
called the “python” command in the terminal it defaulted to Python2. This is a problem
when trying to using Pip and Pipenv. Thus, a fix I found was to call Pipenv commands
by adding “Python3 -m ” in front of the call.

```
python3 -m pipenv --version
```

You might not encounter this problem though. Check your version of Python with

```
python --version
```

Now with NPM, Pipenv, and Python3 down, we have PostgreSql,

```
“a free and open-source relational database management system emphasizing extensibility
and SQL compliance.”
```

### Some relevant knowledge

I had no idea what a database was when I started. A database basically handles all the
data associated with the front-end. You basically request and send data to the database.
Setting this up was confusing. The instructions weren’t too clear. How I finally
managed to do it was to download PostgreSql for Windows, and during installation I set
up the user to be called “postgres” with password “postgres”. This is upon installation
and not for creating a user later on (databases have users associated with them). I set
up SQL by looking at section 1 of the [tutorial](https://www.postgresqltutorial.com/).
You can learn more as you need to. Only the first section is needed to set up. Once you've
made your server and a database named “pipeline” you’ll be able to actually run the web
app locally. This way you can see local changes you’ve made to the code.

First off, when cloning the project from git, directly clone it. Directly cloning it with
the “git clone” command is the way to go. Or you can use their command to do it. Note that
you must be a contributor to do it. Afterwards, you can install the dependencies. The
dependencies are basically modules that your code needs to work. By executing “npm install”
in the folder (the directory with the package.json file) you are installing all the
dependencies listed in the package.json file.

Really just do the following:

```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
npm install
npx webpack --config webpack.development.config.js
pipenv install --dev
pipenv run python manage.py createcachetable
```

To clarify, Webpack is a module bundler. It basically transforms all the modules and their
dependencies into a static asset. A static asset is something the browser does not change.
This way, you won’t accidentally not have images loaded, etc. Webpack is used because you
can’t use require() on the browser, which is how you load and cache JavaScript modules.
It’ll work fine in Node.JS, just not the browser. Webpack basically creates a copy of your
source code and fills in the dependencies. Images that are needed will be taken and placed
into a folder. It allows you greater control over managing your assets. I’m not going to
speak too much on it because I’m quite new to it too.

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


# Work in Progress, not formatted yet.


Learning Django, Black, Flake8, SQL, etc

First Video: https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

Install Django with “pip install django”
Check with “python3 -m django --version”
“django-admin” for sub commands
Use “django-admin startproject <project name>” to start a project with the basic file structure created

manage.py - allows us to run command line commands

A file with the name of your project
Has 4 files:
	__init__.py an empty file that tells python that this is a python file
	Settings.py This is where you change the settings and configurations
	Urls.py     This is where we set up the mapping for certain urls to where they go
	Wsgi.py	  How python web app communicate

You can see the default website by running “python manage.py runserver”



You can map to different urls (other servers).
Adding more routes? 

Second Video https://www.youtube.com/watch?v=a48xeeo5Vnk&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=2

A single project can contain multiple apps
So, we can make an app and add it to multiple websites

Create a new app with “python manage.py startapp <name of new app>”

Look at the views.py in the new app

From django.shortcuts import render
From django.http import HttpResponse

Created a method to handle request in view. You can return actual html code as a string. But that would be a whole bunch of text. You can instead make a module to be plugged into the method instead.
Then we make a urls.py that maps the home or “” to the views.home method we just made.
The urls.py should import views from current directory
Then we add a path that maps to the ‘blog/’ to the <appName>.urls to the project urls.py, so that the project can go to the urls.py of the app
So it’ll go to the project urls.py then from there chops up the string and goes to the next urls.py (the blog urls.py)

‘/’ makes django redirect to that path, so there is no confusion

Make sure a url path maps to that handle (through a urls.py)


