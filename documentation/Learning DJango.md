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

```
__init__.py is an empty file that tells python that this is a python file.
Settings.py is where you change the settings and configurations.
Urls.py is where we set up the mapping for certain urls to where they go.
Wsgi.py is how python web apps communicate.
```

You can see the default website by running:

```
python manage.py runserver
```


## Applications and Routes

[Video](https://www.youtube.com/watch?v=a48xeeo5Vnk&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=2)

A single project can contain multiple apps. So we can make an app and add it to
multiple web apps.

To create a new app use:

```
python manage.py starapp <name of new app>
```

The series will be creating an app named "blog."

The views.py holds methods that handle requests from users. You can make methods
to return actual html code (In the next video, you'll learn to return templates).
After creating a method to handle a request, you must map a url to the method you
created. Make a urls.py file in the blog folder. It should be the same as the one
in the project directory. The only difference is what is inside the url patterns
list. Add a path that maps "blog/" to the <appName>.urls to the project urls.py,
so that the project urls.py will check the blog app's urls.py too. All this works
by chopping up the url in the user's browser to get to the mapped response.


# Templates

[Video](https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=3)

To use templates, we need to make a template directory in the app directory.

After making the templates directory, add a blog directory inside it. This is just
DJango convention for storing templates.

Now the templates are basically just html files as templates. To make sure you can
use the template, you have to add the blog app to the project's installed apps list in
settings.py. Now we can use those templates in views.py (in blogs app).

First, make sure you import render with:

```
from django.shortcuts import render
```

Then you can plug in the template by returning the object from the render() method.

```
return render(request, 'blog/templateName.html')
```

There can also be a third argument to the render() method. It's basically a dictionary
of arguments to pass in.

An example of the third argument would be "context":

```
posts = [
	{
        'author':"Justin",
        'title':"hey",
        'content':"just a test",
        'date_posted':"now, would usually be a date time object",
    },
    {
        'author':"Noob",
        'title':"bye",
        'content':"ending the test",
        'date_posted':"after now",
    },
]

def home(request):
    Context = {
	"posts": posts,
        "title": "hey",
    }

    return render(request, 'blog/home.html', Context)
```

Now with templates, you can inherit from other templates. This way, you can create a
base template with similar html code. You can have a "base.html" that home.html and
about.html could inherit from.

To have a template inherit from another template, place this at the top of the template
that is inheriting:

```
{% extends "blog/base.html" %}
```

{ } are used to write code. If you have variables, use {{ }}. Now you can have fill it in
in the base.html. You create these fill it in spots with:

```
{% block content %}
{% endblock %}
```

By wrapping unique code in the block in the inheriting template, you override this block.

"Content" is just the name of the block. Now the home.html template inheriting from base.html
can fill it in by making a block too.

base.html
```
<!DOCTYPE html>
<html>
<head>
    {% if title %}
	    <title>Django Blog - {{title}}</title>
    {% else %}
        <title>Django Blog</title>
    {% endif %}
</head>

<body>
	{% block content %} {% endblock content %}
</body>
</html>
```

home.html
```
{% extends "blog/base.html" %}

{% block content %}
    {% for post in posts %}
    {% endfor %}
{% endblock content %}
```

Also note how we can use "title" from context dictionary.