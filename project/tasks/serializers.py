from .models import Tasks, TaskLogs, Notifications, TaskComments
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLogs
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComments
        fields = ['user','text']
