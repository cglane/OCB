# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_attributeemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributeemail',
            name='partner_email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
