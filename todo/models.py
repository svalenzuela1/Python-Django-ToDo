from django.db import models
from authentication.models import User


# Create your models here.
class Task(models.Model):
    class Meta:
        verbose_name_plural = 'tasks'

    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField(null=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Item(models.Model):

    class Meta:
        verbose_name_plural = 'items'

    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
