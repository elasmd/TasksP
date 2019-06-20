from django import forms

from .models import Tasks, TaskLogs, TaskComments


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('name', 'date_deadline',)


class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('id',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = TaskComments
        fields = ('text',)


class TaskTimer(forms.ModelForm):
    class Meta:
        model = TaskLogs
        fields = ('task',)

class TaskLogForm(forms.ModelForm):
    class Meta:
        model = TaskLogs
        fields = ('date_finish','time_active')
