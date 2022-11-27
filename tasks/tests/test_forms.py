from tasks.forms import *
from django.test import TestCase


class CreateTaskFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = Category.objects.create(title='testcat', user=self.user)

    def test_create_task_form_lenth(self):
        form_data = {'title': f"{'x'*100}", 'category': self.category}
        form_data_invalid = {'title': f"{'x'*101}", 'category': self.category}
        form = CreateTaskForm(data=form_data)
        form_invalid = CreateTaskForm(data=form_data_invalid)

        self.assertEquals(form.is_valid(), True)
        self.assertEquals(form_invalid.is_valid(), False)

