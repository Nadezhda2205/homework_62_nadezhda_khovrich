from django.urls import path, include
from issue.views import (
    UserInProjectDelete, 
    UserInProjectAdd, 
    TaskListView, 
    TaskDetailView, 
    TaskUpdateView, 
    TaskCreateView, 
    TaskDeleteView, 
    ProjectListView, 
    ProjectDetailView, 
    ProjectCreateView
)
urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/detail/<int:pk>', TaskDetailView.as_view(), name='task_detail'),
    path('task/update/<int:pk>', TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<int:pk>', TaskDeleteView.as_view(), name='task_delete'),

    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/detail/<int:pk>', ProjectDetailView.as_view(), name='project_detail'),
    path('project/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/task/add/', TaskCreateView.as_view(), name='task_create'),
    
    path('project/<int:pk>/users/add/', UserInProjectAdd.as_view(), name='users_add'),
    path('project/<int:project_pk>/user/<int:user_pk>/delete/', UserInProjectDelete.as_view(), name='user_delete'),
    
]
