# Generated by Django 2.2.10 on 2020-02-14 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("server", "0008_auto_20200214_1430")]

    operations = [migrations.RemoveField(model_name="wfmodule", name="fetch_error")]
