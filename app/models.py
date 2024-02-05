from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django.utils import timezone


class Astronaut(models.Model):
    STATUS_CHOICES = (
        (1, 'Работает'),
        (2, 'Отстранен'),
    )

    name = models.CharField(max_length=100, verbose_name="Имя", blank=True, null=True)
    background = models.TextField(max_length=500, verbose_name="Бэкграунд", blank=True, null=True)
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)

    country = models.CharField(max_length=100, verbose_name="Страна", blank=True, null=True)
    sex = models.CharField(max_length=100, verbose_name="Пол", blank=True, null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="astronauts", default="astronauts/default.jpg", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Астронавт"
        verbose_name_plural = "Астронавты"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Flight(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    astronauts = models.ManyToManyField(Astronaut, verbose_name="Астронавты", null=True)

    mission_name = models.CharField(max_length=100, blank=True, null=True)
    objective = models.CharField(max_length=500, blank=True, null=True)

    is_returned_alive = models.CharField(blank=True, null=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner',
                              null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор",
                                  related_name='moderator', null=True)

    def __str__(self):
        return "Полет №" + str(self.pk)

    class Meta:
        verbose_name = "Полет"
        verbose_name_plural = "Полеты"
        ordering = ('-date_formation',)
