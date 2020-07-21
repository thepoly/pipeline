# Learning DJango Framework

This is documentation following a DJango Series. Each section will have a link to
the video and a summary of the key points.

## Getting Started

[Video](https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)

Install DJango with:

```
pip install django
```

Verify your installation by running a command:

```
python3 -m django --version
```

You can get sub commands with:

```
django-admin
```

To start a project with the basic file structure, use:

```
django-admin startproject <project name>
```

There are a number of files in the folder.

manage.py is a file that allows us to run command line commands.

The folder with your project name has 4 files within.

__init__.py  an empty file that tells python that this is a python file
Settings.py  This is where you change the settings and configurations
Urls.py      This is where we set up the mapping for certain urls to where they go
Wsgi.py	     How python web app communicate

You can see the default website by running:

```
python manage.py runserver
```




