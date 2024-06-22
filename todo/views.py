from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.list import ListView

from .forms import RegisterForm
from .models import ToDoTask, ToDoList


def index(request):
    todos = ToDoTask.objects.all()
    return render(request, 'index.html', {'todos': todos, 'completed_todos': None})


def todo_lists(request):
    items = request.user.todolists.all()
    print(items)
    return render(request, 'todo/todo-lists.html', {'todo_lists': items})


# class TodoLists(LoginRequiredMixin, ListView):
#     template_name = 'todo/todo-lists.html'
#     model = ToDoList
#     context_object_name = 'todo_lists'
#
#     def get_queryset(self):
#         user = self.request.user
#         return user.todolists.all()


def todo_task_list(request):
    todos = ToDoTask.objects.all()
    return render(request, 'index.html', {'todos': todos})


def add_todo(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            ToDoTask.objects.create(text=text)
    return redirect('index')


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


def profile_view(request):
    return render(request, 'user/profile.html')

# def todo_list_view(request):
#     # lists = ToDoList.objects.filter(user=request.user)
#     return render(request, 'todo/todo-list-detail.html', {'lists': None})
#
#
# def todo_task_view(request, list_id):
#     todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
#     tasks = todo_list.tasks.all()
#     return render(request, 'todo/task.html', {'list': todo_list, 'tasks': tasks})
