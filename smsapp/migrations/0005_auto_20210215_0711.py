# Generated by Django 2.1 on 2021-02-15 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0004_auto_20210215_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='EmpNumber',
            field=models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='Employement Number'),
        ),
    ]