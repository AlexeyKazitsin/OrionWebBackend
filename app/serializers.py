from rest_framework import serializers

from .models import *


class AstronautSerializer(serializers.ModelSerializer):
    class Meta:
        model = Astronaut
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    def get_access_token(self, user):
        return self.context.get("access_token", "")

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator', 'access_token')


class FlightsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Flight
        fields = "__all__"


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


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

