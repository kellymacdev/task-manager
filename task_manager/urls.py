from django.urls import path
from django.contrib import admin

from task_manager import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("tasks/", views.tasks, name="my_tasks"),
    path("tasks/<int:task_id>/", views.specific_task, name="specific_task"),
    path('admin/', admin.site.urls),
]
