from django.urls import path
from .views import *
from django.urls import path, include
from django.contrib import admin
#from rest_framework import routers

#router = routers.DefaultRouter()

urlpatterns = [
    #path('api', include(router.urls)),
    # Набор методов для услуг
    path('api/astronauts/search/', search_astronauts),  # GET
    path('api/astronauts/<int:astronaut_id>/', get_astronaut_by_id),  # GET
    path('api/astronauts/<int:astronaut_id>/image/', get_astronaut_image),  # GET
    path('api/astronauts/<int:astronaut_id>/update/', update_astronaut),  # PUT
    path('api/astronauts/<int:astronaut_id>/update_image/', update_astronaut_image),  # PUT
    path('api/astronauts/<int:astronaut_id>/delete/', delete_astronaut),  # DELETE
    path('api/astronauts/create/', create_astronaut),  # POST
    path('api/astronauts/<int:astronaut_id>/add_to_flight/', add_astronaut_to_flight),  # POST

    # Набор методов для заявок
    path('api/flights/search/', search_flights),  # GET
    path('api/flights/<int:flight_id>/', get_flight_by_id),  # GET
    path('api/flights/<int:flight_id>/update/', update_flight),  # PUT
    path('api/flights/<int:flight_id>/update_status_user/', update_status_user),  # PUT
    path('api/flights/<int:flight_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/flights/<int:flight_id>/delete/', delete_flight),  # DELETE


    #м-м
    path('api/flights/<int:flight_id>/delete_astronaut/<int:astronaut_id>/', delete_astronaut_from_flight),  # DELETE

    #async
    path('api/flights/<int:flight_id>/update_crew_health/', update_flight_crew_health), #PUT

]