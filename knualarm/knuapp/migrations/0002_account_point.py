# Generated by Django 2.0.1 on 2018-01-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knuapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='point',
            field=models.FloatField(default=0),
        ),
    ]
