import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta
from ...utils import random_text



def add_astronauts():
    Astronaut.objects.create(
        name="Джон Доу",
        country="Соединенные Штаты",
        experience="Опытный астронавт с множеством космических полетов. Специализируется на выходах в открытый космос и работе с робототехникой.",
        age=45,
        sex="Мужской",
        image="astronauts/7.png"
    )

    Astronaut.objects.create(
        name="Джейн Смит",
        country="Канада",
        experience="Бывший инженер со специализацией в системах космических аппаратов. Выбрана за свои технические навыки и умения решать проблемы.",
        age=38,
        sex="Женский",
        image="astronauts/3.png"
    )

    Astronaut.objects.create(
        name="Михаил Иванов",
        country="Россия",
        experience="Космонавт с обширным опытом в долгосрочных космических полетах. Обучен различным научным экспериментам на борту космических аппаратов.",
        age=50,
        sex="Мужской",
        image="astronauts/1.png"
    )

    Astronaut.objects.create(
        name="Белла Родригес",
        country="Бразилия",
        experience="Врач, специализирующаяся на космической медицине. Проводит эксперименты, связанные с здоровьем человека в условиях невесомости.",
        age=41,
        sex="Женский",
        image="astronauts/8.png"
    )

    Astronaut.objects.create(
        name="Чэн Вэй",
        country="Китай",
        experience="Бывший истребительный летчик, отобранный для тренировок космонавтов. Опыт в управлении космическими аппаратами и навигации.",
        age=36,
        sex="Женский",
        image="astronauts/5.png"
    )

    print("Услуги добавлены")


def add_flights():
    users = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    astronauts = Astronaut.objects.all()

    for _ in range(30):
        flight = Flight.objects.create()
        flight.mission_name = "Полет №" + str(flight.pk)
        flight.objective = random_text(10)
        flight.status = random.randint(2, 5)
        flight.owner = random.choice(users)

        if random.randint(0, 10) > 3:
            flight.is_crew_healthy = random.randint(0, 1)

        if flight.status in [3, 4]:
            flight.date_complete = random_date()
            flight.date_formation = flight.date_complete - random_timedelta()
            flight.date_created = flight.date_formation - random_timedelta()
            flight.moderator = random.choice(moderators)
            flight.is_crew_healthy = random.randint(0, 1)
        else:
            flight.date_formation = random_date()
            flight.date_created = flight.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            try:
                item = AstFlig.objects.create()
                item.cosmetic = flight
                item.substance = random.choice(astronauts)
                #item.is_captain = random.choice([True, False])
                item.save()
            except Exception as e:
                print(e)

        flight.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_astronauts()
        add_flights()
