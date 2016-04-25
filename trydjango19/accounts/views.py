from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    next_page = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if next_page:
            # TODO: should be limited by local domains
            return redirect(next_page)
        return redirect('/')

    context = {"form": form}
    return render(request, "login.html", context)


def register_view(request):
    next_page = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        created_user = authenticate(username=user.username, password=password)
        login(request, created_user)
        if next_page:
            # TODO: should be limited by local domains
            return redirect(next_page)
        return redirect('/')
    context = {
        "form": form
    }
    return render(request, "register.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
