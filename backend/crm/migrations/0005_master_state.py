# Generated by Django 4.0.3 on 2022-05-21 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_alter_register_total_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='state',
            field=models.BooleanField(default=True, verbose_name='state'),
        ),
    ]
