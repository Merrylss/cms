# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-05 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('publicTime', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('modifyTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User')),
            ],
        ),
    ]
