# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-10 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0061_auto_20170807_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameterspec',
            name='def_boolean',
        ),
        migrations.RemoveField(
            model_name='parameterspec',
            name='def_float',
        ),
        migrations.RemoveField(
            model_name='parameterspec',
            name='def_integer',
        ),
        migrations.RemoveField(
            model_name='parameterval',
            name='boolean',
        ),
        migrations.RemoveField(
            model_name='parameterval',
            name='float',
        ),
        migrations.RemoveField(
            model_name='parameterval',
            name='integer',
        ),
        migrations.RenameField(
            model_name='parameterval',
            old_name='string',
            new_name='value',
        ),
        migrations.AlterField(
            model_name='parameterval',
            name='value',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.RenameField(
            model_name='parameterspec',
            old_name='def_string',
            new_name='def_value',
        ),
        migrations.AlterField(
            model_name='parameterspec',
            name='def_value',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='parameterspec',
            name='def_menu_items',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parameterspec',
            name='type',
            field=models.CharField(choices=[('string', 'String'), ('integer', 'Integer'), ('float', 'Float'), ('button', 'Button'), ('checkbox', 'Checkbox'), ('menu', 'Menu'), ('column', 'Column'), ('multicolumn', 'Multiple columns'), ('custom', 'Custom')], default='string', max_length=16),
        ),
        migrations.AlterField(
            model_name='parameterval',
            name='menu_items',
            field=models.TextField(blank=True, null=True),
        ),
    ]
