from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import (
  LoginRequiredMixin,
  UserPassesTestMixin
)
from django.contrib.auth import get_user_model 
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
from .forms import CommentCreationForm

# Create your views here.

##########################
# Post Views
##########################

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
# Uses MultipleObjectMixin to allow pagination, FormMixin for forms
class PostDetailView(FormMixin, MultipleObjectMixin, DetailView):
  model = Post

  template_name = 'posts/post_detail.html'
  paginate_by = 5
  form_class = CommentCreationForm

  # Allows multiple models
  def get_context_data(self, **kwargs):
    object_list = Comment.objects.filter(post=self.get_object()).order_by('-date_posted')
    context = super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
    context['comment_form'] = self.get_form()
    return context

  def get_success_url(self):
    return reverse('post-detail', kwargs={'pk': self.object.pk})
  
  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseForbidden()

    self.object = self.get_object()
    form = self.get_form()
    
    # If the forms are valid, get info and save
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = Post.objects.get(pk=kwargs['pk'])
      comment.author = request.user
      # messages.success(request, f'Comment Created')
      comment.save()
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

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



##########################
# Comment Views
##########################

# Class/object based view for single comments
class CommentDetailView(DetailView):
  model = Comment

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
  
  # Where to go if comment is created
  def get_success_url(self):
    comment = self.get_object()
    return reverse('post-detail', kwargs={'pk': comment.post.id})

  def get_context_data(self, **kwargs):
    context = super(CommentUpdateView, self).get_context_data(**kwargs)

    # Post does exist now, so use the stored post id
    context['post_pk'] = self.get_object().post.id
    return context

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

class CommentListView(ListView):
  model = Comment

  template_name = 'posts/comment_page.html'
  context_object_name = 'comments'
  paginate_by = 5

  # Narrow the query set for displaying a user profile
  def get_queryset(self):
    post_pk = username=self.kwargs.get('pk')
    return Comment.objects.filter(post=Post.objects.get(pk=post_pk)).order_by('-date_posted')

# class CommentCreateView(LoginRequiredMixin, CreateView):
#   model = Comment
#   fields = ['comment']

#   # Assign the current user as the author
#   def form_valid(self, form):
#     form.instance.author = self.request.user

#     # Get post using pk in url
#     form.instance.post = Post.objects.get(pk=self.kwargs['pk'])

#     return super().form_valid(form)
  
#   def get_success_url(self):
#     return reverse('comment-create', kwargs={'pk': self.kwargs['pk']})
  
#   # Allows multiple models
#   def get_context_data(self, **kwargs):
#     context = super(CommentCreateView, self).get_context_data(**kwargs)

#     # Comment does not exist yet, so use the url for post id
#     context['post_pk'] = self.kwargs['pk']
#     context['comments'] = Comment.objects.filter(post=Post.objects.get(pk=self.kwargs['pk'])).order_by('-date_posted')
#     return context