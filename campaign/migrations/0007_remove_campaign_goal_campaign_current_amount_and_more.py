# Generated by Django 5.1.1 on 2024-09-10 21:36

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0006_alter_campaign_end_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='goal',
        ),
        migrations.AddField(
            model_name='campaign',
            name='current_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='campaign',
            name='goal_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='subtitle',
            field=models.CharField(default='', max_length=256, verbose_name='subtitle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='video',
            field=models.FileField(null=True, upload_to='campaigns/videos/%Y/%m', validators=[django.core.validators.FileExtensionValidator(['video/mov', 'video/mpeg', 'video/avi', 'video/3gp', 'video/wmv', 'video/flv', 'video/mp4'])], verbose_name='video'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 1, 21, 36, 25, 545053, tzinfo=datetime.timezone.utc), verbose_name='end date '),
        ),
        migrations.CreateModel(
            name='CampaignCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='campaign.campaigncategory', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'campaign category',
                'verbose_name_plural': 'campaign categories',
                'db_table': 'campaign_category',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='campaign.campaigncategory', verbose_name='category'),
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('description', models.TextField(max_length=256, verbose_name='description')),
                ('amount', models.PositiveIntegerField(verbose_name='amount')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reward',
                'verbose_name_plural': 'rewards',
                'db_table': 'reward',
            },
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('returned', 'Returned')], default='pending', max_length=16, verbose_name='status')),
                ('stripe_payment_intent_id', models.CharField(max_length=255, unique=True, verbose_name='stripe payment intent id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='campaign.campaign', verbose_name='campaign')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('reward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='campaign.reward', verbose_name='reward')),
            ],
            options={
                'verbose_name': 'investment',
                'verbose_name_plural': 'investments',
                'db_table': 'investment',
            },
        ),
    ]
