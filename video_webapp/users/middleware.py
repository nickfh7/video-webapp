from django.shortcuts import redirect, reverse
from django.conf import settings
from posts.models import Post
from django.urls import resolve
import datetime, os

# Middleware that makes the user always log in
def AuthRequiredMiddleware(get_response):
  # Can put one time initializations here

  # middleware for requiring login
  def middleware(request):
    response = get_response(request)

    # Allow user to continue if logged in
    # Does not redirect if on the admin, login, or register page without being logged in
    if request.path.startswith('/admin/logout'):
      return redirect('admin:login')
    elif request.path.startswith('/admin/'):
      return response
    elif request.user.is_authenticated or request.path == reverse('login') or request.path.startswith('/favicon.ico'):
      return response
    elif not request.user.is_authenticated and request.path == reverse('register'):
      return response
    else:
      return redirect('login')

  return middleware

# Middleware that logs user activity
def LoggingMiddleware(get_response):

  def middleware(request):
    response = get_response(request)

    try:

      current_url = resolve(request.path_info).url_name

      # Only log data if the user is authenticated and is accessing a post
      if request.user.is_authenticated and current_url == 'post-detail' and request.method == 'GET':
        # Get the log directory
        LOG_DIRECTORY = settings.LOGGING_ROOT + '/user_activity.log'

        # Get the post pk from substring of /posts/<int:pk>
        post_pk = int(str(request.path)[7:-1])

        # Data to store
        log_data = {
          "user_ip"    : str(request.user.user_ip),
          "path"       : str(request.path),
          "post_name"  : str(Post.objects.get(pk=post_pk)),
          "time_stamp" : str(datetime.datetime.now()),
        }

        # Write to log file
        log_file = open(LOG_DIRECTORY, 'a')
        log_file.write(str(log_data))
        log_file.close()

    except Exception as e:
      print("Failed to log: " + str(e))

    finally:
      return response

  return middleware