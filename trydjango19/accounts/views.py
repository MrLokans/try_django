from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


from .forms import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

    context = {"form": form}
    return render(request, "login.html", context)


def register_view(request):
    context = {}
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
