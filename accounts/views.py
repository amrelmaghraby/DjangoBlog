# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

#Create your views here.
def login_view(request):
    title = "login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        print user
        login(request, user)
        return redirect("/posts/")
    return render(request, "login.html", {"form": form, "title": title})

def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username,password=password)
        login(request, new_user)
        return redirect("/posts/")
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "register.html",context)

def logout_view(request):
    logout(request)
    return redirect("/login/")
