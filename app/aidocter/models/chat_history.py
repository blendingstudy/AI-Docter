from django.db import models

class ChatHistory(models.Model):
    
    chat_list = models.ForeignKey("aidocter.chatList", on_delete=models.CASCADE, default=0)
    username = models.CharField(max_length=100)
    message = models.TextField(default='', null=True)
    div = models.CharField(default='', max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = 'chat_history'

