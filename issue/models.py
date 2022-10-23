from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Status(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50, null=False)

    def __str__(self) -> str:
        return self.name


class Type(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50, null=False)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(verbose_name='Название проекта', max_length=50, null=False)
    description = models.TextField(verbose_name='Описание', null=True)
    start_date = models.DateField(verbose_name='Дата начала', null=False)
    end_date = models.DateField(verbose_name='Дата окончания', null=True)
    users = models.ManyToManyField(to=User, verbose_name='Пользователи', blank=True, related_name='projects', null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    summary = models.CharField(verbose_name='Заголовок', max_length=200, null=False)
    description = models.TextField(verbose_name='Описание', null=True)
    status = models.ForeignKey(to='issue.Status', verbose_name='Статус', related_name='status', on_delete=models.RESTRICT)
    type = models.ForeignKey(to='issue.Type', verbose_name='Тип', related_name='type', on_delete=models.RESTRICT)
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    project = models.ForeignKey(to='issue.Project', verbose_name='Проект', related_name='tasks', on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return self.summary
