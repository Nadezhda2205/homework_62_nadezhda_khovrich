from django import forms

from issue.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description',  'status',  'type', 'project']


class SearchTaskForm(forms.Form):
    search = forms.CharField(required=False, label='')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
