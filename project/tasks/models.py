from django.contrib.auth.models import User
from django.db import models


class Tasks(models.Model):
    name = models.CharField(max_length=200)
    usercreation = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='creation')
    assign = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='assign')
    date_deadline = models.DateTimeField()
    date_assign = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)


class TaskLogs(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=True)
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(null=True)
    time_active = models.FloatField(null=True)


class TaskComments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)


class Notifications(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='user')
    user_trigger = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='trigger')
    action_type = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
