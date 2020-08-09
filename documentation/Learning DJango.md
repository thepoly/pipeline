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

The video also goes into using snippets of Html/CSS. I did not note those down, as
it is not relevant. But, if you want, please do look into it. The video provides
very useful snippets. You can break them down.


## Admin Page

[Video](https://www.youtube.com/watch?v=1PkNiYlkkjo&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=4)

This video is short and to the point. It basically goes over what the admin page is,
how you can create users, and how to manage some access. The admin page comes with
DJango and is very useful for making changes to the backend that would otherwise be
cumbersome.

The first time you access the admin page, you need to create a new user. Do so with:

```
python manage.py createsuperuser
```

It won't work if you don't have a database set up. We can get a database set up if
one isn't set up already by calling:

```
python manage.py makemigrations
```
This basically tells DJango to detect changes and prepare to run changes

Then use the migrate command to propagate changes.

```
python manage.py migrate
```

The very first time, it will create some default tables for you and the database.

In the admin page, you can create more users, with varying access levels and modify
existing users.


## Database and Migrations

[Video](https://www.youtube.com/watch?v=aHC3uTkT9r8&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=5)

DJango has its own ORM, or object relational mapper. It allows us to access our database
in an easy manner without using database specific calls. This helps unify the calls to
querying from the database. This way, we can have multiple databases easily and not have
to change our querying code if we change the database we use.

We can represent our database structures as classes or models.

Look at the models.py in the app folder. This is where you add your classes / models.
So now, instead of using dummy data in views.py, we can instead make a class in
modelsy.py.

```
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```

title in this case can be a string of max length 100.
content is just a textfield, meaning unlimited size.
date_posted is a DateTime object. In this case, we set the default to be the current
time. May sure to import timezone to use the above code snippet.

```
from django.utils import timezone
```

We can actually do the same thing with:

```
date_posted = models.DateTimeField(auto_now=True)
```

The problem with this is that you can not modify this later on.

"on_delete=models.CASCADE" makes a user with a foreign key. on_delete specifies that
when the user is deleted, delete the posts.

Now doing this is actually making changes to the database. Thus, you have to make
migrations. Do so by:

```
python manage.py makemigrations
python manage.py migrate
```

This just checks for migrations that can be made and preps it. Then it applies the
migrations with the second command. Now if you look at the migrations folder, you'll
see a new file called "0001_initial.py". This is the migration. You can look inside
to see how the code works with the database.

You can see it as sql query code by executing:
```
python manage.py sqlmigrate appName 0001
```

Now that we set that up, we actually have to create some posts. To do so, enter into
the interactive shell with:
```
python manage.py shell
```

Now import the model you made and the User class, so that we can use them.

```
from blog.models import Post
from django.contrib.auth.models import User
```

To see the users you can use the first command. Then you can filter it to get your
desired user.
```
user.objects.all()
user = User.objects.filter(username='username').first()
```
Note that we filter by username and it returns a list. We then take the first item
in the list. "user" is just a variable we made. Variables are wiped everytime we
exit() the shell. Also note that changes are only applied when we exit the shell.

We can similarly see the Post objects with:

```
Post.objects.all()
```

It'll return an empty list for now because we didn't make anything yet. Try:

```
post_1 = Post(title='Blog 1', content='First Post Content!', author=user)
post_1.save()

post_2 = Post(title="Blog 2", content="Second Post Content!", author_id=user.id)
post_2.save()

user.post_set

user.post_set.create(title=”Blog 3”, content=”Third Post Content!”)
```

We first create a post with the following fields. Then we save it so that we can
actually query it. Else, the change won't be reflected. The second post is just
to show that you can fill in the author field with the user id. user.post_set
is in the user.modelname_set format. It gives all the posts with the user as the
author. The third way to create a post is to actually use the user and create a
post to the user's post_set. It automatically fills in the user as the author.

Note that all the post objects had the date time field automatically filled in
already by our timezone call.

Now to switch from using dummy data to querying our database. Change the Context
dictionary to:

```
Context = {
        'posts': Post.objects.all()     
    }
```

### Side Note
You can actually change the how the date time object displays the date. You can
refer to the [documentation](https://www.youtube.com/redirect?redir_token=QUFFLUhqazZuYVRxX0xZM1BLTE9JakpyVXQ0dUNFTDVQZ3xBQ3Jtc0tsdTBRSjRod2JnREZzaHN1VUIza3pOUmNTaGRXUEwxbFN1UGpHSzVYbEtOdVpPaWp0Z0VvaFZZQU9PQmhTUkNDUWc4bENFWmlDQ3N4UEt0cTI4SnQyZVdSOFQ4ZlVUYURHZklTWC0xRG9GZ0lYTEE2Zw%3D%3D&q=https%3A%2F%2Fdocs.djangoproject.com%2Fen%2F2.0%2Fref%2Ftemplates%2Fbuiltins%2F%23date&event=video_description&v=aHC3uTkT9r8) for more info.

Now you can actually add the model to the admin page. This lets you modify and
create posts in the admin page. Do so by going to the "admin.py" file and
adding your model. In this case it would be:

```
admin.site.register(Post)
```

## User Registration / Forms

[Video](https://www.youtube.com/watch?v=q4jPR-M0TAQ&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=6)


User Registration / Making an admin page for other users

We start off by making a new app to control user registration

“python3 manage.py startapp users”

Add it to the installed apps list in settings

We will create the URL Pattern after making the view

To make the view create a form would be very complicated generally. But DJango already has forms for us.

```
from django.contrib.auth.forms import UserCreationForm
```

Create the template
Create a templates folder and the users sub directory
```
{% extends "blog/base" %}
 
{% block content %}
    <div class="content-section">
        <form method="POST">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">
                    Join Today!
                </legend>
                {{ form.as_p }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type ="submit">
                    Sign Up
                </button>
            </div>
        </form>
        <div class="border-top pt-3">
            <small class="text-muted">
                Already Have An Account?
                <a class="ml-2" href="#">Sign In</a>
            </small>
        </div>
    </div>
{% endblock content %}
```
First thing to note, we can actually still extend our template for the blog app.

All the class attributes in the code are just for styling.
The csrf token provides protection against certain attacks.
We can print the form by simply calling it. The as_p method just prints the form in paragraph tags.

We have the views.py register() as so:
```
def register(request):
    form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})
```

Now let's add the URL Pattern
Here we do it by importing the view directly.
```
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('', include('blog.urls')), # a path to map to your blog app
]
```

Currently, if we enter any info, the form just redirects us to the same page. It doesn’t store any of the info.

We need to do something with the data.

```
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
 
# Create your views here.
 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})
```

So we now add a conditional, that if there is data from POST, we make a form with the data given.

Cleaned_data is the data from the form in dictionary form. We can access this to retrieve data written.

Now let's add a flash message to show success. We can import the messages class and use the success message. These are the types of messages we can use:
```
messages.debug
messages.info
messages.success
messages.warning
messages.error
```

It should look like this now:

```
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
 
# Create your views here.
 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})
```

Now make it redirect to blog home
```
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
 
# Create your views here.
 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})
```

To make sure that messages are printed, add this before the content block in the base.html:
```
{% if messages %}
              {% for message in messages %}
              <div class="alert alert-{{ message.tags}}">
                {{ message }}
              </div>
              {% endfor %}
            {% endif %}
```

Message.tags gets the specific type of message and uses the corresponding css class.

Now let’s use the other fields.

Add in the “forms.save()”

```
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
 
# Create your views here.
 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})
```

Now we want to add in more fields. To do this, we actually have to inherit from forms and then add the fields. So create a new class that inherits UserCreationForm and add fields to it.

```
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
 
    class Meta:
        model = User
        fields = ['username', 'password1','email', 'password2']
```

Now, change all the instances of UserCreationForm to UserRegisterForm.

The rest of the video is just for styling.














