from django.shortcuts import redirect

# This makes the user always log in
def AuthRequiredMiddleware(get_response):
  # Can put one time initializations here

  # middleware for requiring login
  def middleware(request):
    response = get_response(request)

    # Allow user to continue if logged in
    if request.user.is_authenticated:
      return response
    else:
      return redirect('login')

  return middleware