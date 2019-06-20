from datetime import timedelta

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .helpers import notificationadd, taskcommentcontext
from .forms import TaskForm, TaskAssignForm, CommentForm, TaskTimer, TaskLogForm
from .serializers import TaskSerializer, TaskLogSerializer, NotificationSerializer, CommentsSerializer
from .models import Tasks, TaskComments, TaskLogs, Notifications
from django.utils import timezone


@api_view(['GET'])
def tasksview(request):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 50
    queryset = Tasks.objects.order_by('id')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = TaskSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class TasksIndex(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        form = TaskForm(request.POST)
        if form.is_valid():
            Tasks.objects.create(name=form.cleaned_data.get('name'),
                                 usercreation=request.user.id,
                                 date_deadline=form.cleaned_data.get('date_deadline'))
            return JsonResponse({"info": "Task Created"})
        else:
            return JsonResponse({"info": "Task was not created"})

    @staticmethod
    def delete(request):
        form = TaskAssignForm(request.POST)
        if form.is_valid():
            if Tasks.objects.filter(id=form.data.get('id')):
                Tasks.objects.filter(id=form.data.get('id')).delete()

                return JsonResponse({"info": "Task Deleted"})
            else:
                return JsonResponse({"info": "Wrong Id"})
        else:
            JsonResponse(form.errors)


class TasksMe(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        latest_task_list = Tasks.objects.filter(assign=request.user)
        response = []
        for task in latest_task_list:
            response.append(TaskSerializer(task).data)
        return JsonResponse(response, safe=False)

    @staticmethod
    def post(request):

        form = TaskAssignForm(request.POST)
        dateassign = timezone.now()
        if form.is_valid():
            if Tasks.objects.filter(id=form.data.get('id')):
                Tasks.objects.filter(id=form.data.get('id')).update(
                    date_assign=dateassign, assign=request.user)
                notificationadd(request, 1, form.data.get('id'))
                return JsonResponse({"info": "Task assigned"})
            else:
                return JsonResponse({"info": "Wrong Id"})
        else:
            JsonResponse(form.errors)


@api_view(['GET'])
def taskscompletedview(request):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 50
    queryset = Tasks.objects.filter(completed=True).order_by('id')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = TaskSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class TasksCompleted(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        form = TaskAssignForm(request.POST)
        if form.is_valid():
            current_task = Tasks.objects.get(id=form.data.get('id'))
            if current_task:
                if current_task.completed:
                    return JsonResponse({"info": "Task already completed"})
                Tasks.objects.filter(id=form.data.get('id')).update(completed=True)
                notificationadd(request, 3, form.data.get('id'))
                return JsonResponse({"info": "Task Completed"})
            else:
                return JsonResponse({"info": "Wrong Id"})
        else:
            JsonResponse(form.errors)


@api_view(['GET'])
def commentsview(request, task_id):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 50
    queryset = TaskComments.objects.filter(task_id=task_id).order_by('date_created')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = CommentsSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class TasksComments(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, task_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                tasklink = Tasks.objects.get(id=task_id)
            except Tasks.DoesNotExist:
                return JsonResponse({"info": "Wrong task id"})
            TaskComments.objects.create(text=form.data.get('text'),
                                        task=tasklink, user=request.user)
            notificationadd(request, 2, tasklink.id)
            return JsonResponse({"info": "Comment Created"})
        return JsonResponse({"info": "Comment not created"})


@api_view(['GET'])
def notifview(request):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 50
    queryset = Notifications.objects.filter(user=request.user).order_by('-date_created')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = NotificationSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class Notification(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        Notifications.objects.filter(user=request.user).update(seen=True)
        return JsonResponse({'info': 'Notifications seen'})


class TaskTimingStart(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        form = TaskTimer(request.POST)
        if not form.data.get('task'): return JsonResponse({"info": "No task id"})
        if TaskLogs.objects.filter(task_id=form.data.get('task'), user=request.user,
                                   activated=True).exists():
            return JsonResponse({"info": "Timer already started"})
        TaskLogs.objects.create(task_id=form.data.get('task'),
                                date_start=timezone.now(),
                                user=request.user, )
        return JsonResponse({"info": "Timer started"})


class TaskTimingStop(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        form = TaskTimer(request.POST)
        if not form.data.get('task'): return JsonResponse({"info": "No task id"})
        available_tasks = TaskLogs.objects.filter(task_id=form.data.get('task'))

        for task1 in available_tasks:
            if task1.activated:
                date_fin = timezone.now()
                duration = (date_fin - task1.date_start).total_seconds() / 60
                TaskLogs.objects.filter(id=task1.id).update(activated=False,
                                                            date_finish=date_fin,
                                                            time_active=duration)
        return JsonResponse({"info": "Timer stopped"})


@api_view(['GET'])
def tasktimelogview(request, task_id):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 50
    queryset = TaskLogs.objects.filter(task_id=task_id).order_by('-date_finish')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = TaskLogSerializer(result_page, many=True)
    timelog = TaskLogs.objects.filter(task_id=task_id)
    total_time = 0
    for timelogs in timelog:
        total_time += timelogs.time_active
    response1 = {'list': serializer.data, 'total_time': total_time}
    return paginator.get_paginated_response(response1)


class TaskTimeLog(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, task_id):
        form = TaskLogForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date_finish')
            active = form.cleaned_data.get('time_active')
            TaskLogs.objects.create(task_id=task_id, date_start=date,
                                    date_finish=date, time_active=active,
                                    user=request.user, activated=False, )
            return JsonResponse({'info': 'Tasklog added'})
        return JsonResponse({'info': 'Tasklog not added'})


@api_view(['GET'])
def loglastmonth(request):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 50
    last_month = timezone.now() - timedelta(days=30)
    queryset = TaskLogs.objects.filter(date_finish__gte=last_month). \
        order_by('-date_finish')
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = TaskLogSerializer(result_page, many=True)
    total_time = 0
    for timelogs in queryset:
        total_time += timelogs.time_active
    response1 = {'list': serializer.data, 'total_time': total_time}
    return paginator.get_paginated_response(response1)


class LongestTasks(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        response = []
        last_month = timezone.now() - timedelta(days=30)
        timelogs = TaskLogs.objects.filter(date_finish__gte=last_month) \
            .order_by('-date_finish')
        latest_task_list = Tasks.objects.order_by('id')
        for tasks in latest_task_list:
            tasktimeduration = 0
            for timelog in timelogs:
                if tasks.id == timelog.task_id:
                    tasktimeduration += timelog.time_active
            tasktime = {'task_id': tasks.id, 'duration': tasktimeduration}
            response.append(tasktime)
        response.sort(key=lambda i: i['duration'], reverse=True)
        return JsonResponse(response[:20], safe=False)
