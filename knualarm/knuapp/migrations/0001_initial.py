# Generated by Django 2.0.1 on 2018-01-30 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(max_length=128)),
                ('idx', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Announ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='bision_singwan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='dormi_choen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='dreem_singwan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='school_choen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='school_singwan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='school_yesan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='staff_choen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='staff_singwan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='staff_yesan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
