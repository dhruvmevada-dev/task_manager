from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class AuthTest(APITestCase):
    def test_register_and_login(self):
        res = self.client.post(reverse('register'),
                               {'username': 'dev', 'email': 'd@x.com', 'password': 'secret123'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.post(reverse('login'), {'username': 'dev', 'password': 'secret123'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

    def test_tasks_require_auth(self):
        res = self.client.get(reverse('task-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pass12345')
        self.other = User.objects.create_user('bob', password='pass12345')
        res = self.client.post(reverse('login'), {'username': 'alice', 'password': 'pass12345'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
        self.task = Task.objects.create(owner=self.user, title='Mine', priority='high')
        self.other_task = Task.objects.create(owner=self.other, title='Theirs')

    def test_list_only_own_tasks(self):
        res = self.client.get(reverse('task-list'))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'Mine')

    def test_create_task(self):
        data = {'title': 'New', 'description': 'd', 'due_date': '2026-12-01',
                'priority': 'low', 'status': 'pending'}
        res = self.client.post(reverse('task-list'), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.get(title='New').owner, self.user)

    def test_update_task(self):
        data = {'title': 'Updated', 'description': '', 'due_date': '2026-12-01',
                'priority': 'low', 'status': 'completed'}
        res = self.client.put(reverse('task-detail', args=[self.task.id]), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_delete_task(self):
        res = self.client.delete(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_access_others_task(self):
        res = self.client.get(reverse('task-detail', args=[self.other_task.id]))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
