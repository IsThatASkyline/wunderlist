from rest_framework import serializers
from tasks.models import Tasks
from django.contrib.auth.models import User


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Tasks
        fields = ['url', 'id', 'title', 'is_done', 'content', 'user']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'tasks']