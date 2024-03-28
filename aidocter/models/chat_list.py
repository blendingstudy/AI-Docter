from django.db import models

class ChatList(models.Model):
    
    username = models.CharField(max_length=100)
    last_message = models.TextField(default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = 'chat_list'

