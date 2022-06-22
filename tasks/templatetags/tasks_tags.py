from django import template
from django.db.models import *
from tasks.models import Category
from tasks.forms import CreateCategoryForm

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('tasks/list_categories.html', takes_context=True )
def show_categories(context):
    request = context['request']
    category_id = int(str(request.path).split('/')[1])
    user_id = request.user.id
    form = CreateCategoryForm(initial={'user': user_id})
    categories = Category.objects.filter(user_id=user_id).annotate(cnt=Count('tasks', filter=Q(tasks__user_id__exact=user_id)))
    if len(categories) >= 2 :
        first_category = categories[0].pk
        second_category = categories[1].pk
        return {"categories": categories, "cat_form": form, "category_id": category_id,
                "first_category": first_category, "second_category": second_category}

    return {"categories": categories, "cat_form": form, "category_id": category_id, "user_id": user_id}


