from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User, auth


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username , password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('drafts')
        else:
            messages.info(request, 'Usuario o contraseña son incorrectos')
            return redirect('login')
        
    return render(request, 'login.html')