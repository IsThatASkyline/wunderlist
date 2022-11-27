from rest_framework.test import APITestCase
from django.urls import reverse
from tasks.models import *
from rest_framework.authtoken.models import Token


class TestView(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='testuser', password='test1234')
        self.user1_category = Category.objects.create(title='Test_cat', user=self.user1)
        self.user1_category2 = Category.objects.create(title='Test_cat2', user=self.user1)
        self.user1_task = Tasks.objects.create(title='Test_task', category=self.user1_category, user=self.user1)
        self.user1_task2 = Tasks.objects.create(title='Test_task2', category=self.user1_category, user=self.user1)

    def authenticate(self):
        token = Token.objects.get(user__username='testuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))

    def test_task_list_GET(self):
        self.authenticate()
        response = self.client.get(reverse('task_list'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 2)

    def test_task_detail_GET(self):
        self.authenticate()
        response = self.client.get(reverse('task_detail', kwargs={'pk': 1}))
        task = response.data

        self.assertEquals(response.status_code, 200)
        self.assertEquals((task['id'], task['title']), (1, 'Test_task'))

    def test_category_list_POST(self):
        self.authenticate()
        response = self.client.get(reverse('category_list'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 2)

    def test_category_detail_POST(self):
        self.authenticate()
        response = self.client.get(reverse('category_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 2)

    def test_create_task_POST(self):
        self.authenticate()
        response = self.client.post(reverse('category_detail', kwargs={'pk': 1}), {
            'title': 'newtask'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['title'], 'newtask')

    def test_create_category_POST(self):
        self.authenticate()
        response = self.client.post(reverse('category_list'), {
            'title': 'newcat'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['title'], 'newcat')

    def test_delete_task_DELETE(self):
        self.authenticate()
        response = self.client.delete(reverse('task_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.client.get('api/v1/tasks/1/').status_code, 404)

    def test_delete_category_DELETE(self):
        self.authenticate()
        response = self.client.delete(reverse('category_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.client.get('api/v1/categories/1/').status_code, 404)

    def test_update_task_PATCH(self):
        self.authenticate()
        response = self.client.patch(reverse('task_detail', kwargs={'pk': 1}), {'title': 'edit_title',
                                                                                'is_done': True,
                                                                                'content': 'edit_content'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals((response.data['title'], response.data['is_done'], response.data['content']), ('edit_title', True, 'edit_content'))

    def test_NA_task_list_GET(self):
        response = self.client.get(reverse('task_list'))

        self.assertEquals(response.status_code, 401)

    def test_NA_task_detail_GET(self):
        response = self.client.get(reverse('task_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 401)

    def test_NA_category_list_POST(self):
        response = self.client.get(reverse('category_list'))

        self.assertEquals(response.status_code, 401)

    def test_NA_category_detail_POST(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 401)

    def test_NA_create_task_POST(self):
        response = self.client.post(reverse('category_detail', kwargs={'pk': 1}), {
            'title': 'newtask'
        })

        self.assertEquals(response.status_code, 401)

    def test_NA_create_category_POST(self):
        response = self.client.post(reverse('category_list'), {
            'title': 'newcat'
        })

        self.assertEquals(response.status_code, 401)

    def test_NA_delete_task_DELETE(self):
        response = self.client.delete(reverse('task_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 401)

    def test_NA_delete_category_DELETE(self):
        response = self.client.delete(reverse('category_detail', kwargs={'pk': 1}))

        self.assertEquals(response.status_code, 401)

    def test_NA_update_task_PATCH(self):
        response = self.client.patch(reverse('task_detail', kwargs={'pk': 1}), {'title': 'edit_title',
                                                                                'is_done': True,
                                                                                'content': 'edit_content'})
        self.assertEquals(response.status_code, 401)

