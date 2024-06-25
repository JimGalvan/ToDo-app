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
    todos = None
    todo_added = False
    todo_list = None
    if text:
        user = request.user
        todo_list = get_object_or_404(ToDoList, id=list_id, user=user)
        todo_list.tasks.create(list=list_id, title=text)
        todos = todo_list.tasks.all()
        todo_added = True

    completed_status_list, todo_status_list = sort_todos(todos)

    context = {
        'todo_status_list': todo_status_list,
        'completed_status_list': completed_status_list,
        'todo_list': todo_list,
        'list': 'todo_list'
    }

    return render(request, 'todo/partials/todo-tasks.html', context)


@login_required
def toggle_todo(request, list_id, todo_id):
    user = request.user
    todo_list = user.todolists.get(id=list_id)
    todo = todo_list.tasks.get(id=todo_id)

    if todo.status == ToDoTask.TODO:
        todo.status = ToDoTask.COMPLETE
        todo.save()
    else:
        todo.status = ToDoTask.TODO
        todo.save()

    todos = todo_list.tasks.all()
    todo_list = todo_list

    completed_status_list, todo_status_list = sort_todos(todos)

    context = {
        'todo_status_list': todo_status_list,
        'completed_status_list': completed_status_list,
        'todo_list': todo_list
    }

    return render(request, 'todo/partials/todo-tasks.html', context)


def sort_todos(todos):
    todo_status_list = [task for task in todos if task.status == 'TODO']
    completed_status_list = [task for task in todos if task.status == 'COMPLETE']
    return completed_status_list, todo_status_list


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
    todos = todo_list.tasks.all()

    completed_status_list, todo_status_list = sort_todos(todos)

    context = {
        'todo_status_list': todo_status_list,
        'completed_status_list': completed_status_list,
        'todo_list': todo_list,
        'list': 'todo_list'
    }

    return render(request, 'todo/todo-list-tasks.html', context)
