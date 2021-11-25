from django.db import models
from process.models import Process

# CHAT
class Messages(models.Model):
  chat_id = models.IntegerField(default=0)
  text = models.TextField(blank=False, default='')
  fromTelegram = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def last_messages(self,chat_id, n):
    return Messages.objects.filter(chat_id=chat_id).order_by('-created_at').all()[:n][::-1]


class Chat(models.Model):
  chat_id = models.IntegerField(default=0)
  first_name = models.CharField(max_length=70, blank=False, default='')
  last_name = models.CharField(max_length=70, blank=False, default='')
  username = models.CharField(max_length=70, blank=False, default='')

# TASKS
