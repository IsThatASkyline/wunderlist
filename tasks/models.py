from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your models here.



class Tasks(models.Model):
    title = models.CharField(max_length=100, verbose_name="To-Do")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_done = models.BooleanField(default=False, verbose_name='Is done')
    category = models.ForeignKey('Category', verbose_name="Category", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=300, verbose_name="Content", blank=True)

    def get_absolute_url(self):
        return reverse_lazy('view_tasks', kwargs={"category_id": self.category.id, "pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Название категории")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"category_id": self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']
