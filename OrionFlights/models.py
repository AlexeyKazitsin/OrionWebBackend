from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_moderator = models.BooleanField(blank=True, null=True)
    email = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        db_table = 'users'
        app_label = 'OrionFlights'


# Create your models here.
class Flights(models.Model):
    STATUS_CHOICES = (
        (1, 'Черновик'),  # ??????? Изменить на нормальные статусы
        (2, 'Удален'),
        (3, 'Сформирован'),
        (4, 'Завершен'),
        (5, 'Отклонен')
    )
    flight_id = models.AutoField(primary_key=True)
    mission_name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100, blank=True, null=True)
    objective = models.CharField(max_length=1000, blank=True, null=True)
    flight_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date_of_creation = models.DateTimeField(verbose_name="Дата создания", default=timezone.now())
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_of_completion = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='flights_user_set',
                             blank=True, null=True)
    moderator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='flights_moderator_set', blank=True,
                                  null=True)

    class Meta:
        db_table = 'flights'
        app_label = 'OrionFlights'


class Astronauts(models.Model):
    astronaut_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    background = models.CharField(max_length=2000)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=20)
    image = models.TextField(blank=True, null=True)
    #image = models.ImageField(upload_to="images/", blank=True, null=True)
    is_suspended = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        db_table = 'astronauts'
        app_label = 'OrionFlights'


class AstronautFlight(models.Model):
    astronaut = models.ForeignKey(Astronauts, on_delete=models.CASCADE, blank=True, null=True)
    flight = models.ForeignKey(Flights, on_delete=models.CASCADE, blank=True, null=True)
    is_captain = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'astronaut_flight'
        app_label = 'OrionFlights'
