# Generated by Django 5.0.3 on 2024-03-27 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidocter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlist',
            name='last_chat',
            field=models.TextField(default=''),
        ),
    ]