from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('', views.index, name='index'),

]

todo_urlpatterns = [
    path('todo-lists/', views.todo_lists, name='todo_lists'),
    path('add/', views.add_todo, name='add_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('todo-list/', views.todo_task_list, name='todo_task_list'),
]

urlpatterns += todo_urlpatterns
