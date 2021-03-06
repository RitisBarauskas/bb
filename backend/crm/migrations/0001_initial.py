# Generated by Django 4.0.3 on 2022-04-10 20:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCRM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telegram', models.CharField(max_length=100, unique=True, verbose_name='telegram')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='phone')),
                ('role', models.CharField(choices=[('client', 'Клиент'), ('admin', 'Администратор'), ('director', 'Директор')], default='client', max_length=15, verbose_name='role')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='description')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'crm_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('photo', models.CharField(blank=True, default=None, max_length=150, verbose_name='photo')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='phone')),
                ('telegram', models.CharField(default=None, max_length=100, unique=True, verbose_name='telegram')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
                'db_table': 'crm_master',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.SmallIntegerField(db_index=True, verbose_name='cost')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.master')),
            ],
            options={
                'verbose_name': 'Стоимость',
                'verbose_name_plural': 'Стоимость',
                'db_table': 'crm_price',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='name')),
                ('image', models.CharField(blank=True, default=None, max_length=150, verbose_name='image')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'db_table': 'crm_service',
            },
        ),
        migrations.CreateModel(
            name='WorkingHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.DateTimeField(verbose_name='entry')),
                ('state', models.BooleanField(default=True, verbose_name='state')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crm.master')),
            ],
            options={
                'verbose_name': 'Рабочие часы',
                'verbose_name_plural': 'Рабочие часы',
                'db_table': 'crm_working_hours',
                'unique_together': {('master', 'entry')},
            },
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info_date', models.DateTimeField(auto_now_add=True, verbose_name='Date creation entry')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date updating entry')),
                ('price_cost', models.SmallIntegerField(verbose_name='Стоимость по прайсу')),
                ('discount', models.FloatField(blank=True, default=0, verbose_name='Скидка')),
                ('total_sum', models.SmallIntegerField(blank=True, verbose_name='Стоимость услуги к оплате')),
                ('payment_type', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Банковская карта'), ('online', 'Онлайн'), ('transfer', 'Перевод'), ('barter', 'Бартер'), ('other', 'Иное'), ('unknown', 'Не указана')], default='unknown', max_length=30, verbose_name='Способ оплаты')),
                ('regret', models.TextField(blank=True, verbose_name='Пожелание клиента')),
                ('comment', models.TextField(blank=True, verbose_name='Примечание')),
                ('state', models.CharField(choices=[('new_register', 'Новая запись'), ('approved', 'Запись подтверждена'), ('rejected', 'Запись отменена'), ('canceled', 'Клиент не пришел'), ('rendered', 'Услуга оказана'), ('other', 'Статус не указан')], default='new_register', max_length=30, verbose_name='Статус записи')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='clients', to=settings.AUTH_USER_MODEL)),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='price', to='crm.price')),
                ('working_hour', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='working_hours', to='crm.workinghours')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
                'db_table': 'crm_register',
            },
        ),
        migrations.AddField(
            model_name='price',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.service'),
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together={('master', 'service')},
        ),
    ]
