from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import CreateTasksForm, UserRegisterForm, UserLoginForm, CreateCategoryForm, UpdateTaskForm, UpdateTaskContentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Tasks, Category, User
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
            user = form.save()
            new_category = Category.objects.create(title='Incoming', user=User.objects.get(pk=user.id))
            new_category.save()
            new_task = Tasks.objects.create(title='Enjoy!', category=Category.objects.get(pk=new_category.id), user=User.objects.get(pk=user.id))
            new_task.save()
            login(request, user)
            return redirect('category', new_category.id)
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
    username = request.user.username
    return render(request, 'tasks/home.html', context={'username': username})

@login_required
def create_category(request):
    if request.method == "POST" and is_ajax(request=request):
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            new_cat = Category.objects.last()
            new_cat_id = new_cat.id
            return JsonResponse({"title": title, "new_cat_id": new_cat_id}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)


@method_decorator(login_required, name='get')
class TasksByCategoryView(ListView):
    model = Tasks
    template_name = "tasks/my_category.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return Tasks.objects.filter(category_id=self.kwargs['category_id'], user_id=self.request.user).select_related('category').order_by('is_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['form'] = CreateTasksForm()
        context['cat_form'] = CreateCategoryForm()
        context['user'] = self.request.user
        context['username'] = self.request.user.username
        return context
@login_required
def delete_category(request, pk):
    user = request.user.id
    Category.objects.get(pk=pk).delete()
    return redirect('home')


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Tasks
    fields = ['title']

    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_id']
        form.instance.user = self.request.user
        self.object = form.save()
        return JsonResponse({'title': self.object.title,
                             'category_id': self.object.category_id,
                             'new_task_id': self.object.pk}, status=200)

@method_decorator(login_required, name='get')
class TaskDetailView(DetailView):
    model = Tasks
    template_name = "tasks/tasks_detail.html"
    context_object_name = 'target_task'

    def get_context_data(self, **kwargs):
        task = get_object_or_404(Tasks, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['form'] = CreateTasksForm()
        context['tasks'] = Tasks.objects.filter(category_id=self.kwargs['category_id'], user_id=self.request.user).select_related('category').order_by('is_done')
        context['cat_form'] = CreateCategoryForm()
        context['update_form'] = UpdateTaskForm()
        context['update_content_form'] = UpdateTaskContentForm(initial={'content': task.content})
        context['user'] = self.request.user
        context['username'] = self.request.user.username
        context['pk'] = self.kwargs['pk']
        return context


@login_required
def update_task(request, pk):
    task = Tasks.objects.get(pk=pk)
    title = request.POST['title']
    task.title = title
    task.save()
    return JsonResponse({"title": title}, status=200)

@login_required
def update_content(request):
    pk = request.POST['task_id']
    task = Tasks.objects.get(pk=pk)
    task.content = request.POST['content']
    task.save()
    return redirect('view_tasks', task.category_id, pk)

@login_required
def change_checkbox(request):
    if request.method == "POST":
        if request.POST['is_done'] == 'true':
            is_done = True
        else:
            is_done = False

        id = request.POST['id']
        task = Tasks.objects.get(pk=id)
        title = task.title
        category_id = task.category_id
        task.is_done = is_done
        task.save()
        print(f"Task {id} saved with status: {is_done}")
        return JsonResponse({"title": title, "category_id": category_id, "new_task_id": id}, status=200)
    else:
        print('Упсссс....')

    return render(request, 'tasks/home_tasks_list.html')

@login_required
def delete_task(request, pk):
    task = Tasks.objects.get(pk=pk)
    category_id = task.category_id
    task.delete()
    return redirect('category', category_id)
