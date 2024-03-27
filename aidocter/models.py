from django.db import models
from django.utils import timezone

class ChatList(models.Model):
    
    username = models.CharField(max_length=100)
    last_chat = models.TextField(default='', null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    
    class Meta:
        db_table = 'chat_list'

