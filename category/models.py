from django.db import models
from process.models import Process
from django.contrib.auth.models import User

class Category(models.Model):
  name = models.CharField(max_length=200, blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)