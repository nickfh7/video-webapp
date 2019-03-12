from django.shortcuts import redirect, reverse

# Middleware that makes the user always log in
def AuthRequiredMiddleware(get_response):
  # Can put one time initializations here

  # middleware for requiring login
  def middleware(request):
    response = get_response(request)

    # Allow user to continue if logged in
    # Does not redirect if on the admin, login, or register page without being logged in
    if request.path.startswith('/admin/logout'):
      print("REDIRECT a")
      return redirect('admin:login')
    elif request.path.startswith('/admin/'):
      print("REDIRECT b")
      return response
    elif request.user.is_authenticated or request.path == reverse('login')  or request.path.startswith('/favicon.ico'):
      print("RESPONSE 1")
      return response
    elif not request.user.is_authenticated and request.path == reverse('register'):
      print("RESPONSE 3")
      return response
    else:
      print("REDIRECT c")
      return redirect('login')

  return middleware
