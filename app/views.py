import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


user = CustomUser.objects.get(pk=102)
#print(user)



def get_draft_flight():
    flight = Flight.objects.filter(status=1).first()

    if flight is None:
        return None

    return flight


@api_view(["GET"])
def search_astronauts(request):
    query = request.GET.get("query", "")
    sexquery = request.GET.get("sexquery", "")

    astronaut = Astronaut.objects.filter(status=1).filter(name__icontains=query, sex__icontains=sexquery)

    serializer = AstronautSerializer(astronaut, many=True)

    draft_flight = get_draft_flight()

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
def update_astronaut(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_astronaut(request):
    serializer = AstronautSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)


@api_view(["DELETE"])
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
def add_astronaut_to_flight(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)

    draft_flight = get_draft_flight()

    if draft_flight is None:
        draft_flight = Flight.objects.create()
        draft_flight.owner = user
        print(draft_flight.owner)
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
def update_astronaut_image(request, astronaut_id):
    if not Astronaut.objects.filter(pk=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    astronaut = Astronaut.objects.get(pk=astronaut_id)
    serializer = AstronautSerializer(astronaut, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def search_flights(request):
    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start", -1)
    date_end = request.GET.get("date_end", -1)

    flights = Flight.objects.exclude(status__in=[1, 5])

    if status_id != -1:
        flights = flights.filter(status=status_id)

    if date_start != -1:
        flights = flights.filter(date_formation__gte=parse_datetime(date_start))

    if date_end != -1:
        flights = flights.filter(date_formation__lte=parse_datetime(date_end))

    serializer = FlightSerializer(flights, many=True) #FlightsSerializer

    return Response(serializer.data)


@api_view(["GET"])
def get_flight_by_id(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight)

    return Response(serializer.data)


@api_view(["PUT"])
def update_flight(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_flight_crew_health(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)
    serializer = FlightSerializer(flight, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, flight_id):
    if not Flight.objects.filter(pk=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    flight = Flight.objects.get(pk=flight_id)

    flight.status = 2
    flight.date_formation = timezone.now()
    flight.save()

    #calculate_crew_health(flight_id)

    serializer = FlightSerializer(flight)

    return Response(serializer.data)


def calculate_crew_health(flight_id):
    data = {
        "flight_id": flight_id
    }

    requests.post("http://127.0.0.1:8080/calc_crew_health/", json=data, timeout=3)


@api_view(["PUT"])
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
    flight.save()

    serializer = FlightSerializer(flight)

    return Response(serializer.data)


@api_view(["DELETE"])
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
def delete_astronaut_from_flight(request, flight_id, astronaut_id):
    if not AstFlig.objects.filter(flight_id=flight_id, astronaut_id=astronaut_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstFlig.objects.get(flight_id=flight_id, astronaut_id=astronaut_id)
    item.delete()

    flight = Flight.objects.get(pk=flight_id)

    serializer = FlightSerializer(flight)

    return Response(serializer.data)



@api_view(["PUT"])
def update_astronaut_in_flight(request, flight_id, astronaut_id):
    if not AstFlig.objects.filter(astronaut_id=astronaut_id, flight_id=flight_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AstFlig.objects.get(astronaut_id=astronaut_id, flight_id=flight_id)

    serializer = AstFligSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)