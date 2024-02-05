import psycopg2
from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from .models import *
from django.shortcuts import redirect
from django.db.models import Q

AstronautsData = {
    'astronaut': [
        {
            'id': 0,
            'name': 'Александр Иванов',
            'sex': 'Мужской',
            'text': 'Вырос во Владивостоке, с детства увлекался космосом. Окончив университет в Москве по аэрокосмической инженерии, он присоединился к Роскосмосу и стал ключевым членом программы Orion. Его экспертиза в астронавигации и лидерские качества сделали его незаменимым для миссии, а его страсть к космосу привлекает внимание молодежи через блог о своих космических приключениях.',
            'image': 'astro1.jpg',
            'age': '30',
            'country': 'Россия',
        },
        {
            'id': 1,
            'name': 'Исмаэль Гонсалес',
            'sex': 'Мужской',
            'text': 'Родился в Буэнос-Айресе, стал увлечен космосом благодаря отцу и первому взгляду в телескоп. Получив образование по астронавигации и инженерии, он присоединился к национальной космической программе и был отобран для миссии Orion благодаря своим уникальным способностям в инженерии и работе в экстремальных условиях. Вне работы он активно пропагандирует науку среди молодежи, стремясь вдохновить будущее поколение космических исследователей.',
            'image': 'astro2.jpg',
            'age': '40',
            'country': 'США',
        },
        {
            'id': 2,
            'name': 'Лена Шмидт',
            'sex': 'Женский',
            'text': 'Выросла в Берлине, проявила удивительные математические способности и страсть к космосу с ранних лет. Окончив университет с астрономическим образованием, она присоединилась к международной космической программе и была выбрана для участия в миссии Orion благодаря своему уникальному пониманию астрономии и инженерии. Вне работы на космической станции, Лена усердно работает над пропагандой науки среди молодежи, стремясь вдохновить будущее поколение исследователей вселенной.',
            'image': 'astro3.jpg',
            'age': '50',
            'country': 'США',
        },
        {
            'id': 3,
            'name': 'Синх Мехта',
            'sex': 'Мужской',
            'text': 'Вырос в Мумбаи, проявил ранний интерес к космосу, который вдохновил его на изучение аэрокосмической инженерии в Индийском институте технологий. Его инновационные разработки в космической индустрии привлекли внимание международных агентств, и он был отобран для участия в миссии Orion благодаря своему выдающемуся инженерному мышлению. Вне космических экспедиций, он усердно работает над вдохновением молодых умов через свой блог о будущем космических исследований.',
            'image': 'astro4.jpg',
            'age': '60',
            'country': 'Индия',
        },
    ]
}


def GetAstronaut(request, id):
    data_by_id = Astronauts.objects.filter(is_suspended=False).get(astronaut_id=id)
    return render(request, "astronaut.html", {
        'astronaut': data_by_id
    })


def GetAstronauts(request):
    astronauts = Astronauts.objects.filter(is_suspended=False).order_by('-astronaut_id')
    query_astronauts = request.GET.get('query_astronauts')

    if query_astronauts:
        # фильтруем данные по полям "name"
        filtered_data = astronauts.filter(
            Q(name__icontains=query_astronauts))
    else:
        filtered_data = astronauts.all()
        query_astronauts = ""

    return render(request, "astronauts.html", {'filtered_data': filtered_data, 'search_value': query_astronauts})


def DeleteAstronaut(request, id):
    '''astronaut = Astronauts.objects.get(astronaut_id=id)
    astronaut.is_suspended = True
    astronaut.save()
    return redirect('astronauts')'''
    conn = psycopg2.connect(dbname="orion", host="localhost", user="student", password="root", port="5432")
    cursor = conn.cursor()
    cursor.execute("UPDATE \"astronauts\" SET is_suspended=\'true\' WHERE astronaut_id = %s", [id])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('astronauts')

