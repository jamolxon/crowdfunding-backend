# Generated by Django 5.1.1 on 2024-09-10 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0005_chatmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigndata',
            name='social_media_presence',
        ),
        migrations.AddField(
            model_name='campaigndata',
            name='user_id',
            field=models.CharField(default='default_user', max_length=256, verbose_name='user id'),
            preserve_default=False,
        ),
    ]
