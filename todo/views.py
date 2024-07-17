from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import QueryDict
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
    todo_list = None

    if text:
        user = request.user
        todo_list = get_object_or_404(ToDoList, id=list_id, user=user)
        todo_list.tasks.create(list=list_id, title=text)
        todos = todo_list.tasks.all()

    # sort by updated_at field in descending order
    todos = todos.order_by('-sort_timestamp')

    sorted_todos = sorted(todos, key=lambda x: x.order)

    context = {
        'todo_list_items': sorted_todos,
        'todo_list': todo_list,
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
    todos = todos.order_by('-sort_timestamp')

    sorted_todos = sorted(todos, key=lambda x: x.order)

    context = {
        'todo_list_items': sorted_todos,
        'todo_list': todo_list,
    }
    return render(request, 'todo/partials/todo-tasks.html', context)


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

    # sort by updated_at field in descending order
    todos = todos.order_by('-sort_timestamp')

    sorted_todos = sorted(todos, key=lambda x: x.order)

    context = {
        'todo_list_items': sorted_todos,
        'todo_list': todo_list,
    }

    return render(request, 'todo/todo-list-tasks.html', context)


@login_required
def delete_todo(request, list_id, todo_id):
    user = request.user
    todo_list = user.todolists.get(id=list_id)
    todo = todo_list.tasks.get(id=todo_id)

    todo.delete()
    todos = todo_list.tasks.all()

    # sort by updated_at field in descending order
    todos = todos.order_by('-sort_timestamp')

    sorted_todos = sorted(todos, key=lambda x: x.order)

    context = {
        'todo_list_items': sorted_todos,
        'todo_list': todo_list,
    }

    return render(request, 'todo/partials/todo-tasks.html', context)


@login_required
def edit_todo(request, list_id, todo_id):
    data = QueryDict(request.body)
    text = data.get('todo')

    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    todos = todo_list.tasks.all()
    todo = todos.get(id=todo_id)

    todo.title = text
    todo.save(update_sort_timestamp=False)

    # sort by updated_at field in descending order
    todos = todos.order_by('-sort_timestamp')

    sorted_todos = sorted(todos, key=lambda x: x.order)

    context = {
        'todo_list_items': sorted_todos,
        'todo_list': todo_list,
    }

    return render(request, 'todo/partials/todo-tasks.html', context)

@login_required
def sort_todo_list(request, list_id):
    todo_pks_order = request.POST.getlist('todo_order')
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    todos = todo_list.tasks.all()

    sorted_todos = []

    for idx, todo_pk in enumerate(todo_pks_order, start=1):
        todo = todos.get(pk=todo_pk)
        todo.order = idx
        todo.save()
        sorted_todos.append(todo)

    context = {
        'todo_list_items': sorted_todos,
        'todo_list': todo_list,
    }

    # Return the rendered template with the context
    return render(request, 'todo/partials/todo-tasks.html', context)

@login_required
def delete_todo_list(request, list_id):
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    todo_list.is_hidden = True
    todo_list.delete()
    todo_lists = ToDoList.objects.filter(user=request.user, is_hidden=False)
    return render(request, 'todo/todo-lists-list.html', {'todo_lists': todo_lists})


@login_required
def edit_todo_list(request, list_id):
    data = QueryDict(request.body)
    text = data.get('name')

    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    todo_list.name = text
    todo_list.save()

    todo_lists = ToDoList.objects.filter(user=request.user, is_hidden=False)
    return render(request, 'todo/todo-lists-list.html', {'todo_lists': todo_lists})

@login_required
def add_todo_list(request):
    ToDoList.objects.create(user=request.user, name=request.POST.get('list_name'))
    todo_lists = ToDoList.objects.filter(user=request.user, is_hidden=False)
    return render(request, 'todo/todo-lists-list.html', {'todo_lists': todo_lists})
