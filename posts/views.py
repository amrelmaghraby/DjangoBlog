# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import posts
from .forms import postsform
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def post_create(request):
    if not request.user.is_authenticated() :
        return redirect("login")
    inputs = request.POST
    form = postsform(request.POST or None)
    if form.is_valid():
        title = form.cleaned_data['title']
        body = form.cleaned_data['body']
        user = request.user
        instance = posts(title=title,body=body,user=user)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        title = "Create Post"
        context = {
            "form": form, "title": title,
        }
        return render(request, "post_form.html", context)

def post_detail(request,id):
    instance = get_object_or_404(posts, id=id)
    instance.author = instance.id
    context = {
        "title": instance.title,
        "instance": instance,
        "auth": instance.author,
    }
    return render(request,"post_detail.html",context)

def post_list(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', None)
        if search_query is None:
            queryset = posts.objects.all()
        else:
            queryset = posts.objects.filter(Q(title__icontains=search_query)| Q(body__icontains=search_query))
    context = {
        "object_list": queryset,
    }

    return render(request,"index.html",context)

def post_update(request, id=None):
    if not request.user.is_authenticated:
        return redirect("login")
    instance = get_object_or_404(posts, id=id)
    form = postsform(request.POST or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_delete(request, id=None):
    if not request.user.is_authenticated:
        return redirect("login")
    instance = get_object_or_404(posts, id=id)
    instance.delete()
    return redirect("list")