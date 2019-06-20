from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Tasks, TaskLogs, TaskComments, Notifications
from django.utils import timezone
from datetime import timedelta


def addUsers():
    for i in range(5, 100):
        username = 'user%d' % i
        User.objects.create(password=i * i * i, username=username)
    return JsonResponse({"info": "added"})


def addTasks(request):
    for i in range(1, 100):
        taskname = 'Task number %d' % (i + 2)
        date = timezone.now() + timedelta(days=1)
        Tasks.objects.create(name=taskname, date_deadline=date,
                             usercreation_id=1)
    return JsonResponse({"info": "added"})


def addComments(request):
    for i in range(1, 100):
        comment = 'haha %d' % i
        TaskComments.objects.create(text=comment, user_id=(i % 5) + 1, task_id=(i % 10) + 1,
                                    )
    return JsonResponse({"info": "added"})


def addTasklog(request):
    for i in range(1, 100):
        datefinish = timezone.now() + timedelta(days=1)
        TaskLogs.objects.create(task_id=2, date_start=datefinish,
                                date_finish=datefinish, time_active=i * i * (i / 1000),
                                user_id=i, activated=False, )


def addNotifications(request):
    for i in range(1, 2000):
        Notifications.objects.create(user_id=(i % 3) + 1, action_type=(i % 3) + 1,
                                     task_id=(i%50)+1, user_trigger_id=(i%50)+1)
