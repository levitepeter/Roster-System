# Generated by Django 3.1.3 on 2020-11-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20201121_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=40),
        ),
    ]
