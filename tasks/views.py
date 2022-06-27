from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import TasksForm, UserRegisterForm, UserLoginForm, CreateCategoryForm, UpdateTaskForm, UpdateTaskContentForm
from django.contrib.auth.decorators import login_required
from .models import Tasks, Category, User
from django.views.generic import ListView

from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse

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
            category = Category.objects.filter(user=user.id)[0].id
            login(request, user)
            return redirect('category', category)
    else:
        form = UserLoginForm()
    return render(request, 'tasks/login.html', {"form": form})

@login_required
def home(request):
    user = request.user.id
    category = Category.objects.filter(user=user)[0].pk
    return redirect('category', category)

@login_required
def create_category(request):
    if request.method == "POST" and is_ajax(request=request):
        form = CreateCategoryForm(request.POST)
        print(list(request.POST.items()))
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            new_cat = Category.objects.last()
            new_cat_id = new_cat.id
            return JsonResponse({"title": title, "new_cat_id": new_cat_id}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

@login_required
def view_category(request, category_id):
    user = request.user.id
    username = request.user.username
    get_object_or_404(Category, user=user, pk=category_id)
    form = TasksForm()
    cat_form = CreateCategoryForm()

    tasks = Tasks.objects.filter(category_id=category_id, user_id=user).select_related('category').order_by('is_done')
    context = {
        'tasks': tasks,
        'form': form,
        'category_id': category_id,
        'user': user,
        'username': username,
        'cat_form': cat_form,
    }

    return render(request, 'tasks/my_category.html', context=context)

@login_required
def delete_category(request, pk):
    user = request.user.id
    cnt_cats = Category.objects.filter(user=user).count()
    categories = Category.objects.filter(user=user)
    if cnt_cats <= 1:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        first_category = categories[0].pk
        second_category = categories[1].pk
        Category.objects.get(pk=pk).delete()
        if pk != first_category:
            return redirect('category', first_category)
        else:
            return redirect('category', second_category)

@login_required
def create_task(request, category_id):
    user = request.user.id
    if request.method == "POST" and is_ajax(request=request):
        form = TasksForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            form.save()
            new_task = Tasks.objects.filter(title=title, user_id=user).first()
            new_task_id = new_task.id
            print("Запрос из create_task_by_category")
            return JsonResponse({"title": title, "category_id": category_id, "new_task_id": new_task_id}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

@login_required
def detail_task(request, category_id, pk):
    form = TasksForm()
    user = request.user.id
    username = request.user.username
    get_object_or_404(Tasks, user=user, pk=pk)
    tasks = Tasks.objects.filter(category_id=category_id, user_id=user).select_related('category').order_by('is_done')
    target_task = Tasks.objects.get(pk=pk)
    update_form = UpdateTaskForm()
    update_content_form = UpdateTaskContentForm(initial={'content': target_task.content})


    context = {
        'tasks': tasks,
        'form': form,
        'update_form': update_form,
        'update_content_form': update_content_form,
        'category_id': category_id,
        'user': user,
        'pk': pk,
        'target_task': target_task,
        'username': username
    }

    return render(request, 'tasks/tasks_detail.html', context=context)

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
    content = request.POST['content']
    task.content = content
    task.save()
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))

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

    #
    return render(request, 'tasks/home_tasks_list.html')

@login_required
def delete_task(request, pk):
    Tasks.objects.filter(pk=pk).delete()
    category_id = request.POST['category_id']
    return redirect('category', category_id)


# def index(request):
#     tasks = Tasks.objects.all()
#     context = {
#         'tasks': tasks,
#         'title': 'Task list'
#     }
#     return render(request, 'tasks/index.html', context=context)

# def get_category(request, category_title):
#     category_id = Category.objects.get(title=category_title.title()).id
#     tasks = Tasks.objects.filter(category_id=category_id)
#
#     return render(request, 'tasks/category.html', context={'tasks': tasks, 'category': category_title})
#
# def view_tasks(request, task_id):
#     # tasks_item = Tasks.objects.get(pk=task_id)
#     tasks_item = get_object_or_404(Tasks, pk=task_id)
#     return render(request, 'tasks/view_tasks.html', {"tasks_item": tasks_item})
# class ViewTasks(DetailView):
#     model = Tasks
#     template_name = 'tasks/tasks_detail.html'
#     context_object_name = 'tasks_item'
# return Tasks.objects.filter(category_id=self.kwargs['category_id'], user_id=self.request.user.id).select_related('category')
# def create_task(request):
#     form = CreateTaskForm()
#     tasks = TestCategory.objects.all()
#     context = {
#         'tasks': tasks,
#         'form': form,
#     }
#     if request.method == "POST" and is_ajax(request=request):
#         form = CreateTaskForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             form.save()
#             return JsonResponse({"title": title}, status=200)
#         else:
#             errors = form.errors.as_json()
#             return JsonResponse({"errors": errors}, status=400)
#
#
#     return render(request, 'tasks/my_create_task.html', context=context)

# def add_task(request):
#     if request.method == 'POST':
#         form = TasksForm(request.POST)
#         if form.is_valid():
#             task = form.save()
#             return redirect(task)
#     else:
#         form = TasksForm()
#     return render(request, 'tasks/add_task.html', {'form': form})
#

#
# class TasksByCategory(ListView):
#     model = Tasks
#     template_name = 'tasks/my_category.html'
#     context_object_name = 'tasks'
#     allow_empty = False
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cat_title'] = Category.objects.get(pk=self.kwargs['category_id'])
#         context['form'] = CreateTaskForm()
#         context['user_id'] = self.request.user.id
#
#         return context
#
#     def get_queryset(self):
#         return Tasks.objects.filter(category_id=self.kwargs['category_id'], user_id=self.request.user.id).select_related('category')
#
#
# class ViewTasks(ListView):
#     model = Tasks
#     # pk_url_kwarg = 'task_id'
#     template_name = 'tasks/tasks_detail.html'
#     context_object_name = 'tasks'
#     allow_empty = False
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['task_title'] = Tasks.objects.get(pk=self.kwargs['pk'])
#         return context
#
#     def get_queryset(self):
#         return Tasks.objects.filter(category_id=self.kwargs['category_id'],
#                                     user_id=self.request.user.id).select_related('category')

# class HomeTasks(ListView):
#     model = Tasks
#     template_name = 'tasks/home_tasks_list.html'
#     context_object_name = 'tasks'
#     extra_context = {'title': 'All Tasks'}
#     mixin_prop = 'hello world'
#
#     def get_queryset(self):
#         return Tasks.objects.filter(user_id=self.request.user.id).select_related('category')
#
#
# class HomeDetails(ListView):
#     model = Tasks
#     template_name = 'tasks/home_details.html'
#     context_object_name = 'tasks'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Tasks.objects.filter(user_id=self.request.user.id).select_related('category')