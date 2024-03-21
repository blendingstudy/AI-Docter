from django.db import models

from django.db import models

class Member(models.Model):
    no = models.AutoField(primary_key=True)  # 자동으로 증가하는 기본키 필드
    id = models.CharField(max_length=100, unique=True)  # 중복되지 않는 아이디 필드
    pw = models.CharField(max_length=100)  # 비밀번호 필드
    name = models.CharField(max_length=100)  # 비밀번호 필드
    
    class Meta:
        db_table = 'member'
