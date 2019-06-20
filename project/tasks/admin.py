from django.contrib import admin

from .models import Tasks,Notifications,TaskComments


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('name', 'assign','date_assign','date_deadline','completed','active')

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('task_id','user','user_trigger','action_type','seen')

@admin.register(TaskComments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('task_id','user','text')


