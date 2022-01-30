from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCRM(AbstractUser):
    """
    Модель пользователя системы взаимоотношения с клиентом (CRM).
    """

    class RoleUser(models.TextChoices):
        USER = 'client', 'Клиент'
        ADMIN = 'admin', 'Администратор'
        DIRECTOR = 'director', 'Директор'

    telegram = models.CharField(
        'telegram',
        max_length=100,
        blank=False,
        default=None,
        unique=True,
    )
    phone = models.CharField(
        'phone',
        max_length=15,
        blank=False,
        unique=True,
    )
    role = models.CharField(
        'role',
        max_length=15,
        blank=False,
        choices=RoleUser.choices,
        default=RoleUser.USER,
    )
    description = models.TextField(
        'description',
        default=None,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'telegram']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'crm_user'

    def __str__(self):
        return self.get_full_name()


class Master(models.Model):
    """
    Класс мастеров, оказывающих какие-либо услуги
    """

    name = models.CharField(
        'name',
        max_length=100,
        blank=False,
    )
    photo = models.CharField(
        'photo',
        max_length=150,
        blank=True,
        default=None,
    )
    phone = models.CharField(
        'phone',
        max_length=15,
        blank=False,
        unique=True,
    )
    telegram = models.CharField(
        'telegram',
        max_length=100,
        blank=False,
        default=None,
        unique=True,
    )
    description = models.TextField(
        'description',
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = 'master'
        verbose_name_plural = 'masters'
        db_table = 'crm_master'

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Услуги, которые оказывают в учреждении
    """

    name = models.CharField(
        'name',
        max_length=150,
        blank=False,
        unique=True,
    )
    image = models.CharField(
        'image',
        max_length=150,
        blank=True,
        default=None,
    )
    description = models.TextField(
        'description',
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'
        db_table = 'crm_service'

    def __str__(self):
        return self.name


class Price(models.Model):
    """
    Стоимость оказываемых услуг конкретными мастерами
    """

    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        null=False,
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=False,
    )
    cost = models.SmallIntegerField(
        'cost',
        null=False,
        db_index=True,
    )
    comment = models.TextField(
        'comment',
        blank=True,
    )

    class Meta:
        verbose_name = 'price'
        verbose_name_plural = 'prices'
        unique_together = 'master', 'service'
        db_table = 'crm_price'

    def __str__(self):
        return f'{self.master} - {self.service} | {self.cost}'


class WorkingHours(models.Model):
    """
    Рабочие часы конкретных мастеров
    """

    master = models.ForeignKey(
        Master,
        on_delete=models.DO_NOTHING,
        null=False,
    )
    entry = models.DateTimeField(
        'entry',
        null=False,
    )
    state = models.BooleanField(
        'state',
        default=True,
    )

    class Meta:
        verbose_name = 'Рабочие часы'
        verbose_name_plural = 'Рабочие часы'
        unique_together = 'master', 'entry'
        db_table = 'crm_working_hours'

    def __str__(self):
        return f'{self.master} - {self.entry}'


class Register(models.Model):
    """
    Журнал записи
    """

    class PaymentType(models.TextChoices):
        CASH = 'cash', 'Наличные'
        CARD = 'card', 'Банковская карта'
        ONLINE = 'online', 'Онлайн'
        DIRECTOR = 'transfer', 'Перевод'
        BARTER = 'barter', 'Бартер'
        OTHER = 'other', 'Иное'
        UNKNOWN = 'unknown', 'Не указана'

    class StateRegister(models.TextChoices):
        NEW_REGISTER = 'new_register', 'Новая запись'
        APPROVED = 'approved', 'Запись подтверждена'
        REJECTED = 'rejected', 'Запись отменена'
        CANCELED = 'canceled', 'Клиент не пришел'
        RENDERED = 'rendered', 'Услуга оказана'
        OTHER = 'other', 'Статус не указан'

    client = models.ForeignKey(
        UserCRM,
        on_delete=models.DO_NOTHING,
        related_name='clients',
        null=False,
    )
    info_date = models.DateTimeField(
        'Date creation entry',
        auto_now_add=True,
    )
    date_update = models.DateTimeField(
        'Date updating entry',
        auto_now=True,
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.DO_NOTHING,
        null=False,
        related_name='masters',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.DO_NOTHING,
        null=False,
        related_name='services',
    )
    working_hour = models.ForeignKey(
        WorkingHours,
        on_delete=models.DO_NOTHING,
        null=False,
    )
    price_cost = models.SmallIntegerField(
        'Стоимость по прайсу',
        null=False,
    )
    discount = models.FloatField(
        'Скидка',
        default=0,
        blank=True,
    )
    total_sum = models.SmallIntegerField(
        'Стоимость услуги к оплате',
        blank=True,
    )
    payment_type = models.CharField(
        'Способ оплаты',
        max_length=30,
        choices=PaymentType.choices,
        default=PaymentType.UNKNOWN,
    )
    regret = models.TextField(
        'Пожелание клиента',
        blank=True,
    )
    comment = models.TextField(
        'Примечание',
        blank=True,
    )
    state = models.CharField(
        'Статус записи',
        max_length=30,
        choices=StateRegister.choices,
        default=StateRegister.NEW_REGISTER,
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        db_table = 'crm_register'

    def __str__(self):
        return f'{self.working_hour.entry} - {self.master.name} - {self.client}'
