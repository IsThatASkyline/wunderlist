from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import *
from .utils import *
from .forms import UserRegisterForm, UserLoginForm


def start(request):
    return redirect('login')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user, category_id = service_register_user(form)
            login(request, user)
            return redirect('category', category_id)
    else:
        form = UserRegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'tasks/login.html', {"form": form})


@login_required
def home(request):
    return render(request, 'tasks/home.html', context={'username': request.user.username})


@method_decorator(login_required, name='post')
class CreateCategoryView(LoginRequiredMixin, CreateCategoryMixin, CreateView):
    model = Category
    fields = ['title']


@method_decorator(login_required, name='get')
class TasksByCategoryView(CategoryContextMixin, GetTasksByCategoryMixin, ListView):
    model = Tasks
    template_name = "tasks/my_category.html"
    context_object_name = 'tasks'


@login_required
def delete_category(request, pk):
    service_delete_catagory(pk)
    return redirect('home')


@method_decorator(login_required, name='post')
class CreateTaskView(LoginRequiredMixin, CreateTaskMixin, CreateView):
    model = Tasks
    fields = ['title']


@method_decorator(login_required, name='get')
class TaskDetailView(TaskContextMixin, DetailView):
    model = Tasks
    template_name = "tasks/tasks_detail.html"
    context_object_name = 'target_task'


@login_required
def update_task(request, pk):
    title = service_update_task_title(pk, request.POST['title'])
    return JsonResponse({"title": title}, status=200)


@login_required
def update_content(request):
    task_id = request.POST['task_id']
    category_id = service_update_task_content(task_id, request.POST['content'])
    return redirect('view_tasks', category_id, task_id)


@login_required
def change_checkbox(request):
    task_id = request.POST['id']
    title, category_id = service_checkbox(task_id, request.POST['is_done'])
    return JsonResponse({"title": title, "category_id": category_id, "new_task_id": task_id}, status=200)


@login_required
def delete_task(request, pk):
    category_id = service_delete_task(pk)
    return redirect('category', category_id)
