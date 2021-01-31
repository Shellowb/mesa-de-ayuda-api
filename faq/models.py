from django.db import models
from process.models import Process
from category.models import Category
from django.contrib.auth.models import User

class FAQs(models.Model):
  question = models.CharField(max_length=200,blank=False, default='')
  answer = models.TextField(blank=False, default='')
  created_at = models.DateTimeField(auto_now_add=True)
  last_update = models.DateTimeField(auto_now_add=True)
  process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
  published = models.BooleanField(default=True)
  likes = models.IntegerField(default=0)
  dislikes = models.IntegerField(default=0)
  created_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='faq_created_by')
  updated_by = models.ForeignKey(User, default=None, blank=True, on_delete=models.DO_NOTHING, related_name='faq_updated_by')
