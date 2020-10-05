from django.db import models
from process.models import Process

class Instance(models.Model):
  name = models.CharField(max_length=200, blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  published = models.BooleanField(default=True)
  process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)
  #created_by = createdBy = models.ForeignKey(User)

class Steps(models.Model):
  start_date = models.DateTimeField()
  end_date = models.DateTimeField(blank=True, null=True)
  name = models.CharField(max_length=200, blank=False, default='')
  description = models.TextField(blank=True, default='')
  instance = models.ForeignKey(Instance, on_delete=models.CASCADE, default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  #created_by = createdBy = models.ForeignKey(User)

class News(models.Model):
  description = models.TextField(blank=False, default='')
  instance = models.ForeignKey(Instance, on_delete=models.CASCADE, default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  #created_by = createdBy = models.ForeignKey(User)