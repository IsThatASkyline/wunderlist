from .models import Tasks, Category, User
from .forms import CreateTasksForm, UserRegisterForm, UserLoginForm, CreateCategoryForm, UpdateTaskForm, UpdateTaskContentForm
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic.edit import FormMixin


class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

class CategoryContextMixin(generic.base.ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['form'] = CreateTasksForm()
        context['cat_form'] = CreateCategoryForm()
        context['user'] = self.request.user
        context['username'] = self.request.user.username
        return context


class TaskContextMixin(CategoryContextMixin):

    def get_context_data(self, **kwargs):
        task = get_object_or_404(Tasks, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['tasks'] = Tasks.objects.filter(category_id=self.kwargs['category_id'], user_id=self.request.user).select_related('category').order_by('is_done')
        context['update_form'] = UpdateTaskForm()
        context['update_content_form'] = UpdateTaskContentForm(initial={'content': task.content})
        context['pk'] = self.kwargs['pk']
        return context


class GetTasksByCategoryMixin(generic.base.ContextMixin):

    def get_queryset(self):
        get_object_or_404(Category, pk=self.kwargs['category_id'])
        return Tasks.objects.filter(category_id=self.kwargs['category_id'], user_id=self.request.user).select_related('category').order_by('is_done')


class CreateTaskMixin(FormMixin):

    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_id']
        form.instance.user = self.request.user
        super().form_valid(form)
        self.object = form.save()
        return JsonResponse({'title': self.object.title,
                             'category_id': self.object.category_id,
                             'new_task_id': self.object.pk}, status=200)
