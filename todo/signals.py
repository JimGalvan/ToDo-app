from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from .enums import DefaultToDoLists
from .models import ToDoList, User


@receiver(post_save, sender=User)
def create_default_todo_lists(sender, instance, created, **kwargs):
    if created:
        default_list_names = DefaultToDoLists.get_values()
        for name in default_list_names:
            if name == DefaultToDoLists.PERSONAL.value:
                ToDoList.objects.create(user=instance, name=name, is_default=True, is_main=True)
            else:
                ToDoList.objects.create(user=instance, name=name, is_default=True)


@receiver(pre_delete, sender=ToDoList)
def ensure_main_list_on_delete(sender, instance, **kwargs):
    if instance.is_main:
        user_lists = ToDoList.objects.filter(user=instance.user, is_hidden=False).exclude(id=instance.id)
        if user_lists.exists():
            new_main_list = user_lists.first()
            new_main_list.is_main = True
            new_main_list.save()


@receiver(post_save, sender=ToDoList)
def ensure_main_list_on_save(sender, instance, **kwargs):
    if not ToDoList.objects.filter(user=instance.user, is_main=True).exists():
        instance.is_main = True
        instance.save()
