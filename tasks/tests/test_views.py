from django.test import TestCase
from django.urls import reverse
from tasks.models import Tasks, Category, User


class TestViews(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.user1_category = Category.objects.create(title='Test_cat', user=self.user1)
        self.user1_task = Tasks.objects.create(title='Test_task', category=self.user1_category, user=self.user1)

    def test_category_GET(self):
        url = reverse('category', kwargs={"category_id": self.user1_category.id})
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/my_category.html')

    def test_task_GET(self):
        url = reverse('view_tasks', kwargs={"category_id": self.user1_category.id, "pk": self.user1_task.pk})
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks_detail.html')

    def test_update_task_content_POST(self):
        url = reverse('update_content')
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        response = self.client.post(url, {'content': 'newcontent',
                                    'task_id': self.user1_task.pk})
        self.assertRedirects(response, '/category/1/task/1/details', status_code=302, target_status_code=200)

    def test_delete_task_POST(self):
        url = reverse('delete_task', kwargs={'pk': self.user1_task.pk})
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        response = self.client.post(url, {'category_id': self.user1_category.pk})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.client.get(reverse('view_tasks', kwargs={"category_id": self.user1_category.id, "pk": self.user1_task.pk})).status_code, 404)

    def test_delete_category_POST(self):
        url = reverse('delete_category', kwargs={'pk': self.user1_category.pk})
        self.client.force_login(User.objects.get_or_create(username='testuser1')[0])
        response = self.client.post(url)

        self.assertRedirects(response, '/home/', target_status_code=200)
        self.assertEquals(self.client.get(reverse('category', kwargs={"category_id": self.user1_category.pk})).status_code, 404)


    def test_category_NA_GET(self):
        url = reverse('category', kwargs={"category_id": self.user1_category.id})
        na_response = self.client.get(url)

        self.assertRedirects(na_response, f'/accounts/login/?next=/category/{self.user1_category.id}/', target_status_code=404)


    def test_task_NA_GET(self):
        url = reverse('view_tasks', kwargs={"category_id": self.user1_category.id, "pk": self.user1_task.pk})
        na_response = self.client.get(url)

        self.assertRedirects(na_response, f'/accounts/login/?next=/category/{self.user1_category.id}/task/{self.user1_task.pk}/details', target_status_code=404)

    def test_update_task_content_NA_POST(self):

        url = reverse('update_content')
        na_response = self.client.post(url, {'content': 'newcontent', 'task_id': self.user1_task.pk})

        self.assertRedirects(na_response, '/accounts/login/?next=/update-task-content/', target_status_code=404)

    def test_delete_task_NA_POST(self):
        url = reverse('delete_task', kwargs={'pk': self.user1_task.pk})
        na_response = self.client.post(url, {'category_id': self.user1_category.pk})

        self.assertRedirects(na_response, f'/accounts/login/?next=/{self.user1_task.pk}/delete_task/', target_status_code=404)

    def test_delete_category_NA_POST(self):
        url = reverse('delete_category', kwargs={'pk': self.user1_category.pk})
        na_response = self.client.get(url)

        self.assertRedirects(na_response, f'/accounts/login/?next=/{self.user1_category.pk}/delete_category/', target_status_code=404)

