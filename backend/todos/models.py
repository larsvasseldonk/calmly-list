from django.db import models
import uuid
import time

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    dueDate = models.BigIntegerField(null=True, blank=True, help_text="Timestamp in milliseconds")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.BigIntegerField(help_text="Timestamp in milliseconds")

    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = int(time.time() * 1000)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
