from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('text', 'completed', 'priority', 'category', 'createdAt')
    list_filter = ('completed', 'priority', 'category')
    search_fields = ('text', 'category')
