# Generated by Django 2.2.2 on 2019-06-17 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190617_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='assign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
