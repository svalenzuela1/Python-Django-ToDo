from rest_framework import serializers
from .models import Task, Item


class ItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Item
        fields = ("id", "user", "task", "name", "description", "completed", "created_at", "updated_at", "is_public")


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    items = ItemSerializer(many=True, read_only=True, required=False) #class from above

    class Meta:
        model = Task
        fields = ('id', 'user', 'name', 'date', 'completed', 'created_at', 'updated_at', 'is_public', 'items')

