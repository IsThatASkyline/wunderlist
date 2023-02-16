from .models import Tasks, Category
from .forms import CreateCategoryForm
from django.contrib.auth.models import User
from .tasks import send_auth_mail



def service_checkbox(task_id, is_done):
    task = Tasks.objects.get(pk=task_id)
    title = task.title
    category_id = task.category_id
    if is_done == 'true':
        task.is_done = True
    elif is_done == 'false':
        task.is_done = False
    task.save()
    return title, category_id


def service_delete_catagory(pk):
    return Category.objects.get(pk=pk).delete()


def service_delete_task(pk):
    task = Tasks.objects.get(pk=pk)
    category_id = task.category_id
    task.delete()
    return category_id


def service_update_task_content(pk, new_content):
    task = Tasks.objects.get(pk=pk)
    task.content = new_content
    task.save()
    return task.category_id


def service_update_task_title(pk, new_title):
    task = Tasks.objects.get(pk=pk)
    task.title = new_title
    task.save()
    return new_title


def service_register_user(form):
    user = form.save()
    category_id = service_create_data_for_new_user(user)
    send_auth_mail.delay(form.instance.email) # Redis must be running
    return user, category_id


def service_create_data_for_new_user(user):
    new_category = Category.objects.create(title='Incoming', user=user)
    new_category.save()
    new_task = Tasks.objects.create(title='Enjoy!', category=Category.objects.get(pk=new_category.id), user=user)
    new_task.save()
    return new_category.id
