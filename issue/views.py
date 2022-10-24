from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from accounts.view import GroupPermission
from django.core.handlers.wsgi import WSGIRequest


from issue.forms import TaskForm, SearchTaskForm, ProjectForm
from issue.models import Task, Project


class SuccessDetailUrlMixin:
    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskListView(GroupPermission, ListView):
    template_name: str = 'task_list.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 3
    paginate_orphans = 1
    groups = ['Project Manager', 'Team Lead', 'Developer']

 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchTaskForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(summary__iregex=self.search_value) | Q(description__iregex=self.search_value)
                )
        return queryset


class TaskDetailView(GroupPermission, LoginRequiredMixin, DetailView):
    template_name: str = 'task_detail.html'
    model = Task
    context_object_name = 'task'
    groups = ['Project Manager', 'Team Lead', 'Developer']


class TaskUpdateView(GroupPermission, LoginRequiredMixin, SuccessDetailUrlMixin, UpdateView):
    template_name = 'task_update.html'
    form_class = TaskForm
    model = Task
    context_object_name = 'task'
    groups = ['Project Manager', 'Team Lead', 'Developer']

    def dispatch(self, request, *args, **kwargs):
        task_pk = kwargs['pk']
        task = Task.objects.get(pk=task_pk)
        project_of_task: Project = task.project
        users_in_project = project_of_task.users.all()
        if not request.user in users_in_project:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TaskCreateView(GroupPermission, LoginRequiredMixin, SuccessDetailUrlMixin, CreateView):
    template_name: str = 'task_create.html'
    model = Task
    fields = ['summary', 'description', 'status', 'type']
    groups = ['Project Manager', 'Team Lead', 'Developer']


    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        project_pk = kwargs['pk']
        project = Project.objects.get(pk=project_pk)
        users_in_project = project.users.all()
        if not request.user in users_in_project:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TaskDeleteView(GroupPermission, LoginRequiredMixin, DeleteView):
    template_name = 'task_delete.html'
    model = Task
    success_url = reverse_lazy('task_list')
    groups = ['Project Manager', 'Team Lead']

    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        task_pk = kwargs['pk']
        task = Task.objects.get(pk=task_pk)
        project_of_task: Project = task.project
        users_in_project = project_of_task.users.all()
        if not request.user in users_in_project:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProjectListView(GroupPermission, ListView):
    template_name: str = 'project/project_list.html'
    model = Project
    context_object_name = 'projects'
    groups = ['Project Manager', 'Team Lead', 'Developer']


class ProjectDetailView(GroupPermission, DetailView):
    template_name: str = 'project/project_detail.html'
    model = Project
    context_object_name = 'project'
    groups = ['Project Manager', 'Team Lead', 'Developer']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context['users'] = users
        return context


class ProjectCreateView(GroupPermission, LoginRequiredMixin, CreateView):
    template_name: str = 'project/project_create.html'
    form_class = ProjectForm
    model = Project
    groups = ['Project Manager']


    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class UserInProjectAdd(GroupPermission, TemplateView):
    groups = ['Project Manager', 'Team Lead']


    def post(self, request, *args, **kwargs):
        project_pk = kwargs.get('pk')
        users_pk = dict(request.POST).get('users')
        project = Project.objects.get(pk=project_pk)
        for user_pk in users_pk:
            project.users.add(User.objects.get(pk=user_pk))
        return redirect('project_detail', pk=project_pk)
        
    def dispatch(self, request, *args, **kwargs):
        project_pk = kwargs['pk']
        project = Project.objects.get(pk=project_pk)
        users_in_project = project.users.all()
        if not request.user in users_in_project:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserInProjectDelete(GroupPermission, TemplateView):
    groups = ['Project Manager', 'Team Lead']
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_pk')
        project_id = kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        project.users.remove(User.objects.get(pk=user_id))
        return redirect('project_detail', pk=project_id)
    
    def dispatch(self, request, *args, **kwargs):
        project_pk = kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        users_in_project = project.users.all()
        if not request.user in users_in_project:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
