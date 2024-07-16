from django.contrib.auth.views import logout_then_login
from django.urls import path

from . import views
from .views import hide_todo_list, set_main_todo_list

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', logout_then_login, {'login_url': '/'}, name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('accounts/profile/', views.profile_view, name='profile'),
]

todo_list_urlpatterns = [
    path('todo-lists/', views.todo_lists, name='todo_lists'),
    path('todo-lists/<int:list_id>/hide/', hide_todo_list, name='hide_todo_list'),
    path('todo-lists/<int:list_id>/todo-tasks/', views.todo_list_tasks, name='todo_list_tasks'),
    path('todo-lists/<int:list_id>/set-main/', set_main_todo_list, name='set_main_todo_list'),
    path('todo-lists/<int:list_id>/sort/', views.sort_todo_list, name='sort'),
    path('todo-lists/<int:list_id>/delete/', views.delete_todo_list, name='delete_todo_list'),
    path('todo-lists/<int:list_id>/edit/', views.edit_todo_list, name='edit_todo_list'),
    path('todo-lists/add/', views.add_todo_list, name='add_todo_list'),
]

urlpatterns += todo_list_urlpatterns

todo_task_urlpatterns = [
    path('todo-lists/<int:list_id>/add_todo/', views.add_todo, name='add_todo'),
    path('todo-lists/<int:list_id>/todo-task/<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('todo-lists/<int:list_id>/todo-task/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('todo-lists/<int:list_id>/todo-task/<int:todo_id>/edit/', views.edit_todo, name='edit_todo'),
    path('todo-lists/<int:list_id>/todo-tasks/', views.todo_list_tasks, name='todo_list_tasks'),
]

urlpatterns += todo_task_urlpatterns
