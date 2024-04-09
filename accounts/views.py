from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import UserRegistrationForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print("done")
        if form.is_valid():
            form.save()
            print(form.data)
            return redirect('login')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # print(form)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"=========={email}{password}")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))  # Redirect to homepage after successful login
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})
