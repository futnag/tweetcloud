# Generated by Django 2.0 on 2018-04-10 02:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(blank=True, verbose_name=datetime.datetime.now)),
            ],
        ),
    ]
