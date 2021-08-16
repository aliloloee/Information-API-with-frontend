from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import UserLoginForm



def logout_user(request) :
    if not request.user.is_authenticated :
        return redirect('accounts:login')
    else :
        logout(request)
    return redirect('accounts:login')

def login_user(request) :
    if request.user.is_authenticated :
        return redirect('interface:home')

    if request.method == 'POST' :
        form = UserLoginForm(request.POST)
        if form.is_valid() :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            # check user_type in order to only let doctors login
            if user != None and user.user_type == 1 :
                login(request, user)
                return redirect('interface:home')
            else :
                messages.add_message(request, messages.ERROR, 'Wrong credentials or not a defined Doctor')

    form = UserLoginForm()
    return render(request, 'registration/login.html', {'form' : form})