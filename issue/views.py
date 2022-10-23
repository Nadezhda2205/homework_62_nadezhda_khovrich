from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


from issue.forms import TaskForm, SearchTaskForm, ProjectForm
from issue.models import Task, Project


class SuccessDetailUrlMixin:
    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})



class TaskListView(ListView):
    template_name: str = 'task_list.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 3
    paginate_orphans = 1

 
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


class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name: str = 'task_detail.html'
    model = Task
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, SuccessDetailUrlMixin, UpdateView):
    template_name = 'task_update.html'
    form_class = TaskForm
    model = Task
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessDetailUrlMixin, CreateView):
    template_name: str = 'task_create.html'
    model = Task
    fields = ['summary', 'description', 'status', 'type']

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'task_delete.html'
    model = Task
    success_url = reverse_lazy('task_list')
    


class ProjectListView(ListView):
    template_name: str = 'project/project_list.html'
    model = Project
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    template_name: str = 'project/project_detail.html'
    model = Project
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name: str = 'task_create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})
