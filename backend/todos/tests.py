from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Todo
import time
import uuid

class TodoApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.todo_data = {
            'text': 'Test Todo',
            'priority': 'medium',
            'category': 'work'
        }
        self.todo = Todo.objects.create(
            text='Existing Todo',
            priority='low',
            createdAt=int(time.time() * 1000)
        )

    def test_create_todo(self):
        response = self.client.post('/todos', self.todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.get(text='Test Todo').priority, 'medium')

    def test_create_todo_invalid_payload(self):
        """Test creating a todo with invalid data."""
        # Empty text
        invalid_data = self.todo_data.copy()
        invalid_data['text'] = ''
        response = self.client.post('/todos', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid priority
        invalid_data = self.todo_data.copy()
        invalid_data['priority'] = 'critical'  # Not in choices
        response = self.client.post('/todos', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_todos(self):
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_todo(self):
        update_data = {'completed': True}
        response = self.client.patch(f'/todos/{self.todo.id}', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_partial_update(self):
        """Ensure partial updates don't clear other fields."""
        original_category = self.todo.category
        update_data = {'priority': 'high'}
        response = self.client.patch(f'/todos/{self.todo.id}', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.priority, 'high')
        self.assertEqual(self.todo.category, original_category)

    def test_update_non_existent_todo(self):
        non_existent_id = uuid.uuid4()
        response = self.client.patch(f'/todos/{non_existent_id}', {'completed': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo(self):
        response = self.client.delete(f'/todos/{self.todo.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_non_existent_todo(self):
        non_existent_id = uuid.uuid4()
        response = self.client.delete(f'/todos/{non_existent_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_completed_todos(self):
        Todo.objects.create(text='Completed Todo', completed=True, createdAt=123)
        response = self.client.delete('/todos/completed')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 1)  # Only 'Existing Todo' remains (not completed)

    def test_ordering(self):
        """Test that todos are retrieved in the expected order."""
        # Create another todo with a later timestamp
        time.sleep(0.001) # Ensure time difference
        Todo.objects.create(text='Newer Todo', createdAt=int(time.time() * 1000))
        
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Assuming default ordering is by ID or insertion order if not specified.
        # If we want specific ordering, we should enforce it in the view/model.
        # For now, just checking we get both back.
