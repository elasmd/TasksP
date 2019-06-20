from rest_framework.pagination import PageNumberPagination

from .models import TaskComments, Notifications, Tasks


def taskcommentcontext(output, task_id, username, dateassign, datedeadline):
    if username:
        context = {'name': output,
                   'task_id': task_id,
                   "assign": username.get_username(),
                   "date_assign": dateassign,
                   "date_deadline": datedeadline,
                   'comments': {}
                   }
    else:
        context = {'name': output,
                   'task_id': task_id,
                   "assign": username,
                   "date_assign": dateassign,
                   "date_deadline": datedeadline,
                   'comments': {}
                   }
    latest_comment_list = TaskComments.objects.filter(task_id=task_id)
    for index, comment in enumerate(latest_comment_list):
        context['comments']['id'] = comment.id
        context['comments']['text'] = comment.text
    return context


def notificationadd(request, action, task):
    if action == 2:
        notiftask = Tasks.objects.get(id=task)
        user = notiftask.assign
        Notifications.objects.create(user=user, action_type=action, task_id=task,
                                     user_trigger=request.user)
    elif action == 1:
        user = request.user
        Notifications.objects.create(user=user, action_type=action, task_id=task,
                                     user_trigger=request.user)
    else:
        notiftask = Tasks.objects.get(id=task)
        latest_comment_list = TaskComments.objects.filter(task_id=notiftask.id)
        for comment in latest_comment_list:
            Notifications.objects.create(user=comment.user, action_type=action, task_id=task,
                                         user_trigger=request.user)


def notificationlist(request):
    latest_not_list = Notifications.objects.filter(user=request.user).order_by(
        '-date_created')
    count_new = 0
    response = []
    actiondone = ''
    for notif in latest_not_list:
        if notif.action_type == 1:
            actiondone = 'Assigned task'
        elif notif.action_type == 2:
            actiondone = 'Commented on your task'
        elif notif.action_type == 3:
            actiondone = 'Commented Task was closed'
        context = {
            "task": notif.task_id,
            "actiondone": actiondone,
            "date": notif.date_created,
            "seen": notif.seen,
        }
        if not notif.seen:
            count_new += 1
        response.append(context)

    return {
        'response': response,
        'unseen': count_new
    }

