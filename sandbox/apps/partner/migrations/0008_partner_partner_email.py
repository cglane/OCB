# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_auto_20171031_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='partner_email',
            field=models.EmailField(default=b'john@email.com', max_length=254, verbose_name='Partner Email'),
        ),
    ]
