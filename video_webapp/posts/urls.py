from django.urls import path
from .views import (
  PostListView, 
  PostDetailView,
  PostCreateView,
  PostUpdateView,
  PostDeleteView,
  UserPostListView,
  CommentCreateView,
  CommentUpdateView,
  CommentDeleteView,
)
from . import views

# URL patterns for each type of page
# <...> indicates variable for URL, pk is the key for the post
urlpatterns = [
    path('', PostListView.as_view(), name="posts-home"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('<int:pk>/new-comment/', CommentCreateView.as_view(), name="comment-create"),
    path('comment/<int:pk>/update', CommentUpdateView.as_view(), name="comment-update"),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name="comment-delete"),
    path('new/', PostCreateView.as_view(), name="post-create"),
    path('<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
]

# This is what it looks for
# <app>/<model>_<viewtype>.html