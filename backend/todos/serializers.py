from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'text', 'completed', 'dueDate', 'priority', 'category', 'createdAt']
        read_only_fields = ['id', 'createdAt']
