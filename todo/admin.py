from django.contrib import admin
from .models import ToDoTask, ToDoList

admin.site.register(ToDoTask)
admin.site.register(ToDoList)