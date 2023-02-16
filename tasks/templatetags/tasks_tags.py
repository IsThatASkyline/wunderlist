from django import template
from django.db.models import *
from tasks.models import Category
from tasks.forms import CreateCategoryForm

register = template.Library()

@register.inclusion_tag('tasks/list_categories.html', takes_context=True )
def show_categories(context):
    request = context['request']
    try:
        category_id = context['category_id']
    except:
        category_id = None
    user_id = request.user.id
    form = CreateCategoryForm(initial={'user': user_id})
    try:
        categories = Category.objects.filter(user_id=user_id).annotate(cnt=Count('tasks', filter=Q(tasks__user_id__exact=user_id)))
    except:
        categories = None
    return {"categories": categories, "cat_form": form, "category_id": category_id, "user_id": user_id}


