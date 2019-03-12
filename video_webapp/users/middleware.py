from django.shortcuts import redirect, reverse

# Middleware that makes the user always log in
def AuthRequiredMiddleware(get_response):
  # Can put one time initializations here

  # middleware for requiring login
  def middleware(request):
    response = get_response(request)

    # Allow user to continue if logged in
    # Does not redirect if on the admin, login, or register page without being logged in
    if request.user.is_authenticated or request.path == reverse('login'):
      return response
    elif request.path.startswith('/admin/'):
      return response
    elif not request.user.is_authenticated and request.path == reverse('register'):
      return response
    else:
      return redirect('login')

  return middleware
