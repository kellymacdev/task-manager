from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
import json
from django.core import paginator
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

from task_manager.models import Task
def index(request):
    return render(request, "task_manager/index.html")

@csrf_exempt
def tasks(request):
    if request.method == "GET":
        all_tasks = Task.objects.filter(user=request.user)
        return JsonResponse([task.serialize() for task in all_tasks], safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        new_task = Task(title=data["title"], description=data["description"], user=request.user)
        new_task.save()
        return JsonResponse(new_task.serialize(), status=201)

@csrf_exempt
def specific_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': "task not found"}, status=404)

    if task.user != request.user:
        return JsonResponse({'error': "not authorized"}, status=403)

    if request.method == "GET":
        return JsonResponse(task.serialize(), status=201)

    elif request.method in ["PUT","PATCH"]:
        data = json.loads(request.body)
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]
        task.save()
        return JsonResponse(task.serialize(), status=201)

    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({'message': "task deleted"}, status=200)

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({'error': "POST request required"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirmation = data.get("confirmation")

    if password != confirmation:
        return JsonResponse({'error': "passwords do not match"}, status=400)

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except IntegrityError:
        return JsonResponse({"message": "Username already taken."}, status=400)
    login(request, user)
    return JsonResponse({'message': "User registered successfully."}, status=201)


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({'error': "POST request required"}, status=400)
        # Attempt to sign user in
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    user = authenticate(request, username=username, password=password)
     # Check if authentication successful
    if user is not None:
        login(request, user)
        return JsonResponse({'message': "User logged in."}, status=200)
    else:
        return JsonResponse({"message": "Invalid username and/or password."}, status=401)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': "User logged out."}, status=200)

