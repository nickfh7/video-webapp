from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm, UserChangePasswordForm
from ipware import get_client_ip

def register(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.user_ip = get_client_ip(request)
      instance.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}!')
      return redirect('login')

  else:
    form = CustomUserCreationForm()
  return render(request, 'users/register.html', {'form': form})

# Handles all profile updates
@login_required
def profile(request):
  # If the profile is being updated
  if request.method == 'POST':
    u_form = CustomUserChangeForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, 
                               request.FILES, 
                               instance=request.user.profile)
    
    # If the forms are valid
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect('profile')

  # Fill in user info on profile page
  else :
    u_form = CustomUserChangeForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
 
  context = {
    'u_form': u_form,
    'p_form': p_form
  }
  return render(request, 'users/profile.html', context)

# Form for changing password
@login_required
def change_password(request):
  if request.method == 'POST':
    form = UserChangePasswordForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)  # Important!
      messages.success(request, 'Your password was successfully updated!')
      return redirect('change_password')
    else:
      messages.error(request, 'Please correct the error below.')
  else:
    form = UserChangePasswordForm(request.user)
  return render(request, 'users/change_password.html', {
    'form': form
  })