import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_flight(request):
    user = identity_user(request)

    if user is None:
        return None

    flight = Flight.objects.filter(owner_id=user.pk).filter(status=1).first()

    if flight is None:
        return None

    return flight


@api_view(["GET"])
def search_astronauts(request):
    query = request.GET.get("query", "")

    astronaut = Astronaut.objects.filter(status=1).filter(name__icontains=query)

    serializer = AstronautSerializer(astronaut, many=True)

    draft_flight = get_draft_flight(request)

    resp = {
        "astronauts": serializer.data,
        "draft_flight_id": draft_flight.pk if draft_flight else None
    }

    return Response(resp)


@api_view(["GET"])
def get_astronaut_by_id(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_astronaut(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_astronaut(request):
    astronaut = Astronaut.objects.create()

    serializer = AstronautSerializer(astronaut)

    return Response(serializer.data)

'''
@api_view(["POST"])
@permission_classes([IsModerator])
def create_astronaut(request):
    serializer = AstronautSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data)
'''

@api_view(["DELETE"])
@permission_classes([IsAuthenticated]) #IsModerator
def delete_astronaut(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    astronaut.status = 2
    astronaut.save()

    astronaut = Astronaut.objects.filter(status=1)
    serializer = AstronautSerializer(astronaut, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_astronaut_to_flight(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    draft_flight = get_draft_flight(request)

    if draft_flight is None:
        draft_flight = Flight.objects.create()
        draft_flight.owner = identity_user(request)
        draft_flight.save()

    if AstFlig.objects.filter(flight=draft_flight, astronaut=astronaut).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = AstFlig.objects.create()
    cons.flight = draft_flight
    cons.astronaut = astronaut
    cons.save()

    serializer = FlightSerializer(draft_flight)

    return Response(serializer.data)


@api_view(["GET"])
def get_astronaut_image(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    return HttpResponse(astronaut.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_astronaut_image(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_flights(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start", -1)
    date_end = request.GET.get("date_end", -1)

    flights = Flight.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        flights = flights.filter(owner_id=user.pk)

    if status_id != -1:
        flights = flights.filter(status=status_id)

    if date_start != -1:
        flights = flights.filter(date_formation__gte=parse_datetime(date_start))

    if date_end != -1:
        flights = flights.filter(date_formation__lte=parse_datetime(date_end))

    serializer = FlightsSerializer(flights, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_flight_by_id(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_flight(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_flight_crew_health(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)




    flight.owner = identity_user(request)
    flight.status = 2
    flight.date_formation = timezone.now()
    flight.save()

    calculate_crew_health(flight_id)

    serializer = FlightSerializer(flight)

    return Response(serializer.data)


def calculate_crew_health(flight_id):
    data = {
        "flight_id": flight_id
    }

    requests.post("http://127.0.0.1:8080/calc_crew_health/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.status = request_status
    flight.date_complete = timezone.now()
    flight.moderator = identity_user(request)   #!!! добавил строчку
    flight.save()

    serializer = FlightSerializer(flight)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_flight(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)

    if flight.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    flight.status = 5
    flight.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_astronaut_from_flight(request, flight_id, astronaut_id):
    if not AstFlig.objects.filter(flight_id=flight_id, astronaut_id=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstFlig.objects.get(flight_id=flight_id, astronaut_id=astronaut_id)
    item.delete()

    flight = Flight.objects.get(pk=flight_id)

    serializer = FlightSerializer(flight)

    return Response(serializer.data)

'''
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    flight.astronauts.remove(Astronaut.objects.get(pk=astronaut_id))
    flight.save()

    if flight.astronauts.count() == 0:
        flight.delete()
        return Response(status=status.HTTP_201_CREATED)

    serializer = FlightSerializer(flight)

    return Response(serializer.data, status=status.HTTP_200_OK)
'''

'''
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_astronaut_in_flight(request, flight_id, astronaut_id):
    if not AstFlig.objects.filter(astronaut_id=astronaut_id, flight_id=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstFlig.objects.get(astronaut_id=astronaut_id, flight_id=flight_id)
    return Response(item.is_captain)
'''


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_astronaut_in_flight(request, flight_id, astronaut_id):
    if not AstFlig.objects.filter(astronaut_id=astronaut_id, flight_id=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstFlig.objects.get(astronaut_id=astronaut_id, flight_id=flight_id)

    serializer = AstFligSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "Введенные данные невалидны"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    serializer = UserSerializer(
        user,
        context={
            "access_token": access_token
        }
    )

    response = Response(serializer.data, status=status.HTTP_200_OK)
    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer) #!!!
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)
    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def check(request):
    user = identity_user(request)

    user = CustomUser.objects.get(pk=user.pk)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')

    return  response