from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegisterForm
from .models import ToDoTask, ToDoList


def index(request):
    todos = ToDoTask.objects.all()
    return render(request, 'index.html', {'todos': todos, 'completed_todos': None})


@login_required
def todo_lists(request):
    items = request.user.todolists.all()
    return render(request, 'todo/todo-lists.html', {'todo_lists': items})


@login_required
def hide_todo_list(request, list_id):
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    if todo_list.is_default:
        todo_list.is_hidden = True
        todo_list.save()
    return redirect('todo_list_view')


@login_required
def todo_list_view(request):
    todo_lists = ToDoList.objects.filter(user=request.user, is_hidden=False)
    return render(request, 'todo_list.html', {'todo_lists': todo_lists})


@login_required
def set_main_todo_list(request, list_id):
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    if not todo_list.is_hidden:
        ToDoList.objects.filter(user=request.user).update(is_main=False)
        todo_list.is_main = True
        todo_list.save()
    return redirect('todo_list_view')


@login_required
def todo_task_list(request):
    todos = ToDoTask.objects.all()
    return render(request, 'index.html', {'todos': todos})


@login_required
def add_todo(request, list_id):
    text = request.POST.get('todo')
    if text:
        user = request.user
        todo_list = get_object_or_404(ToDoList, id=list_id, user=user)
        todo_list.tasks.create(list=list_id, title=text)
    return redirect('index')


@login_required
def toggle_todo(request, todo_id):
    todo = ToDoTask.objects.get(id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('index')


class Login(LoginView):
    template_name = 'registration/login.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


@login_required
def profile_view(request):
    return render(request, 'user/profile.html')


@login_required
def todo_list_tasks(request, list_id):
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    tasks = todo_list.tasks.all()
    return render(request, 'todo/todo-list-tasks.html', {'list': todo_list, 'tasks': tasks, 'todo_list': todo_list})
