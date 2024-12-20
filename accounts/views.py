from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods, require_POST


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get("next") or "homepage:homepage"
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        context = {"login_form": form}
        return render(request, "accounts/login.html", context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("homepage:homepage")
    else:
        form = CustomUserCreationForm()
        context = {"sign_form": form}
        return render(request, "accounts/signin.html", context)


@require_POST
def resign(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout()
    return redirect("homepage:homepage")


@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("homepage:homepage")
    else:
        form = form = CustomUserChangeForm(instance=request.user)

    context = {"form": form}
    return render(request, "accounts/update.html", context)


@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("homepage:homepage")
    else:
        form = PasswordChangeForm(request.user)

    context = {"form": form}
    return render(request, "accounts/change-password.html", context)