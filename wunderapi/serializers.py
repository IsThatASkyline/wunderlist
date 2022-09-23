from rest_framework import serializers
from tasks.models import Tasks, Category
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    category = serializers.ReadOnlyField(source='category.id')
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'is_done', 'content', 'category', 'updated_at', 'user']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Category
        fields = ['id', 'title', 'user']