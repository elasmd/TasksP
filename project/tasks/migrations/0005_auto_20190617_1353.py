# Generated by Django 2.2.2 on 2019-06-17 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20190617_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='user_trigger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trigger', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='assign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assign', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='usercreation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creation', to=settings.AUTH_USER_MODEL),
        ),
    ]
