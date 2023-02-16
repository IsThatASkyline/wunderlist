from tasks.models import *
from django.test import TestCase

class TasksModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = Category.objects.create(title='testcat', user=self.user)
        Tasks.objects.create(title='testtask', category=self.category, user=self.user, content='testcontent')

    def test_get_absolute_url(self):
        task = Tasks.objects.get(pk=1)

        self.assertEquals(task.get_absolute_url(), '/category/1/task/1/details')

    def test_title_length(self):
        task = Tasks.objects.get(pk=1)
        max_length = task._meta.get_field('title').max_length

        self.assertEquals(max_length, 100)

class CategoryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = Category.objects.create(title='testcat', user=self.user)
        Tasks.objects.create(title='testtask', category=self.category, user=self.user, content='testcontent')

    def test_get_absolute_url(self):
        category = Category.objects.get(pk=1)

        self.assertEquals(category.get_absolute_url(), '/category/1/')

    def test_delete_category(self):
        category = Category.objects.get(pk=1)
        tasks_count = Tasks.objects.filter(category=category).count()
        category.delete()

        self.assertEquals(tasks_count, 1)
        self.assertEquals(Category.objects.filter(pk=1).count(), 0)
        self.assertEquals(Tasks.objects.filter(pk=1).count(), 0)