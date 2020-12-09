from django.shortcuts import render

from django.shortcuts import render
from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView
from .models import Post

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'views_list.html'


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        # Retrieve the blog post just using `get_object` functionality.
        obj = super(PostDetailView, self).get_object(queryset)

        # Track the users access to the blog by post!
        Tracker.objects.create_from_request(self.request, obj)

        return obj
