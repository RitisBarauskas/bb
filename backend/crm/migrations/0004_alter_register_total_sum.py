# Generated by Django 4.0.3 on 2022-04-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_remove_register_price_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='total_sum',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Стоимость услуги к оплате'),
        ),
    ]