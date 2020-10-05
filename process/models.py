from django.db import models

class Process(models.Model):
  name = models.CharField(max_length=70, blank=False, default='')
  description = models.TextField(blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now=True)
  published = models.BooleanField(default=True)
  #created_by = createdBy = models.ForeignKey(User)