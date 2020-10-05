from django.db import models
from process.models import Process

class FAQs(models.Model):
  question = models.CharField(max_length=200,blank=False, default='')
  answer = models.TextField(blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now_add=True)
  process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)
  published = models.BooleanField(default=True)
  #created_by = createdBy = models.ForeignKey(User)
