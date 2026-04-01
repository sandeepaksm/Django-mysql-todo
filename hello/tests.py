from django.test import TestCase
from django.urls import reverse
from .models import Todo


class TodoModelTest(TestCase):

    def test_create_todo(self):
        todo = Todo.objects.create(title="Test Todo")
        self.assertEqual(todo.title, "Test Todo")
        self.assertFalse(todo.completed)

    def test_todo_str(self):
        todo = Todo.objects.create(title="My Task")
        self.assertEqual(str(todo), "My Task")


class TodoViewTest(TestCase):

    def test_todo_list_page_loads(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_todo_view(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'Test from view',
            'description': '',
            'completed': False
        })
        self.assertEqual(Todo.objects.count(), 1)
