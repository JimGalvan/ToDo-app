from django.contrib.auth.models import User
from django.db import models


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todolists')
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ToDoTask(models.Model):
    TODO = 'TODO'
    TO_COMPLETE = 'TO_COMPLETE'
    COMPLETE = 'COMPLETE'
    STATUS_CHOICES = [
        (TODO, 'To Do'),
        (TO_COMPLETE, 'To Complete'),
        (COMPLETE, 'Complete'),
    ]

    list = models.ForeignKey(ToDoList, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=TODO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sort_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        update_sort_timestamp = kwargs.pop('update_sort_timestamp', True)
        if update_sort_timestamp:
            self.sort_timestamp = self.updated_at

        super(ToDoTask, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-sort_timestamp']
