from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # home
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'cuentas/login.html')


def logout_view(request):
    logout(request)
    return redirect('/cuentas/login/')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('/cuentas/registro/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('/cuentas/registro/')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect('/')  # home

    return render(request, 'cuentas/registro.html')
