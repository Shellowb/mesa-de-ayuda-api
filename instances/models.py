from datetime import timedelta
import django
from django.db import models
from process.models import Process
from django.contrib.auth.models import User

class Instance(models.Model):
  name = models.CharField(max_length=200, blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  published = models.BooleanField(default=True)
  process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)
  created_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='instance_created_by')
  updated_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='instance_updated_by')

  @staticmethod
  def get_all_published():
    instances = Instance.objects.filter(published=True).order_by('-created_at')
    str_list = ""
    for instance in instances:
      str_list += f'{instance.name} {instance.id}'
    return str_list

  @staticmethod
  def get_instance_by_name(name, publish=True):
    try:
      return Instance.objects.get(name=name, published=publish)
    except Exception as e:
      return None

  def __str__(self):
    publish = 'Sí' if self.published else 'No'
    return f'{self.name} publicada: {publish}'

class Steps(models.Model):
  start_date = models.DateTimeField()
  end_date = models.DateTimeField(blank=True, null=True)
  name = models.CharField(max_length=200, blank=False, default='')
  description = models.TextField(blank=True, default='')
  instance = models.ForeignKey(Instance, on_delete=models.CASCADE, default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='step_created_by')
  updated_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='step_updated_by')

  @staticmethod
  def get_closer_step(instance: Instance):
    steps = Steps.objects.filter(instance=instance)
    closer_step = None
    today = django.utils.timezone.now()
    max_step = django.utils.timezone.now() + timedelta(weeks=52)
    for step in steps:
      if step.end_date >= today:
        if step.end_date < max_step:
          max_step = step.end_date 
          closer_step = step
    return closer_step


class News(models.Model):
  description = models.TextField(blank=False, default='')
  instance = models.ForeignKey(Instance, on_delete=models.CASCADE, default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='news_created_by')
  updated_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='news_updated_by')