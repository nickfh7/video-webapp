from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import (
  LoginRequiredMixin,
  UserPassesTestMixin
)
from django.contrib.auth import get_user_model
from django.views.generic import (
  ListView, 
  DetailView, 
  CreateView,
  UpdateView,
  DeleteView,
)
from django.contrib import messages
from django.urls import reverse
from .models import Post, Comment
# Create your views here.

# Class/object based view for list of posts
class PostListView(ListView):
  model = Post
  
  # This is what it looks for
  # <app>/<model>_<viewtype>.html
  # without below line
  template_name = 'posts/home.html'

  # Find object to iterate over
  context_object_name = 'posts'

  # Order of the objects to list
  ordering = ['-date_posted']

  # Determines the number of posts that are displayed on a given page
  paginate_by = 5

# Same as above, but narrowed by user
class UserPostListView(ListView):
  model = Post

  template_name = 'posts/user_posts.html'
  context_object_name = 'posts'
  paginate_by = 5

  # Narrow the query set for displaying a user profile
  def get_queryset(self):
    user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted')


# Class/object based view for single posts
# Uses more of the default conventions
class PostDetailView(DetailView):
  model = Post

  # Allows multiple models
  def get_context_data(self, **kwargs):
    context = super(PostDetailView, self).get_context_data(**kwargs)
    #context['Post'] = Post
    context['comments'] = Comment.objects.filter(post=Post.objects.get(pk=self.kwargs['pk']))
    return context

class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content', 'video_thumbnail', 'video']

  # Assign the current user as the author
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']

  # Assign the current user as the author
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  # This prevents other users from editing posts that aren't theirs
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  success_url = "/"

  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False

class CommentView(CreateView):
  model = Comment
  fields = ['comment']

  # Assign the current user as the author
  def form_valid(self, form):
    form.instance.author = self.request.user
    form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
    return super().form_valid(form)
  
  def get_success_url(self):
    comment = self.get_object()
    return reverse('post-detail', kwargs={'pk': comment.post.id})
  
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Comment
  fields = ['comment']

  # Assign the current user as the author
  def form_valid(self, form):
    return super().form_valid(form)

  # This prevents other users from editing posts that aren't theirs
  def test_func(self):
    comment = self.get_object()
    if self.request.user == comment.author:
      return True
    return False
  
  def get_success_url(self):
    comment = self.get_object()
    return reverse('post-detail', kwargs={'pk': comment.post.id})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Comment
  
  def test_func(self):
    comment = self.get_object()
    if self.request.user == comment.author:
      return True
    return False

  def get_success_url(self):
    comment = self.get_object()
    return reverse('post-detail', kwargs={'pk': comment.post.id})
