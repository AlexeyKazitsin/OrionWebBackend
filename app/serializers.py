from rest_framework import serializers

from .models import *


class AstronautSerializer(serializers.ModelSerializer):
    class Meta:
        model = Astronaut
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email')



class AstFligSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstFlig
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    astronauts = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_astronauts(self, flight):
        items = AstFlig.objects.filter(flight_id=flight.pk)
        return AstronautSerializer([item.astronaut for item in items], many=True).data

    class Meta:
        model = Flight
        fields = "__all__"




