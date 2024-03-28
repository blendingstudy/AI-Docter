# Generated by Django 5.0.3 on 2024-03-28 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidocter', '0006_delete_chathistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('message', models.TextField(default='', null=True)),
                ('div', models.CharField(default='', max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'chat_history',
            },
        ),
    ]
