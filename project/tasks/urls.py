from rest_framework.routers import SimpleRouter as Router
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt

from . import views, databaseinsert


urlpatterns = [
    path('add/', views.TasksIndex.as_view(), name='index'),
    path('',views.tasksview,name = 'viewindex'),
    path('me/', views.TasksMe.as_view(), name='me'),
    path('complete/',views.taskscompletedview,name='complete'),
    path('completed/', views.TasksCompleted.as_view(), name='completed'),
    path('<int:task_id>/comments/', views.commentsview, name='commentsview'),
    path('<int:task_id>/comment/', views.TasksComments.as_view(), name='comments'),
    path('notifications/', views.Notification.as_view(), name='notifications'),
    path('start/', views.TaskTimingStart.as_view(), name='start'),
    path('stop/', views.TaskTimingStop.as_view(), name='stop'),
    path('<int:task_id>/timelog/', views.TaskTimeLog.as_view(), name='timelog'),
    path('timelogmonth', views.loglastmonth, name='timelog30'),
    path('longest/', views.LongestTasks.as_view(), name='longesttimelog'),
    #path('databaseinsert/', databaseinsert.addTasklog, name='add'),
    path('notif/',views.notifview,name='notif'),
    path('<int:task_id>/timelogs/',views.tasktimelogview,name='timelogs')
]
