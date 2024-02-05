from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        AstFlig.objects.all().delete()
        Flight.objects.all().delete()
        Astronaut.objects.all().delete()
        CustomUser.objects.all().delete()
