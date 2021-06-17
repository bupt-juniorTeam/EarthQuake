from django.db.models import F, Q

from .models import *
from .encode import *


def create_new_earthquake(source, where, when, longitude, latitude):
    Earthquake.objects.create(
        source=source,
        where=get_location_code(where),
        when=when,
        longitude=longitude,
        latitude=latitude
    )


def create_new_set(earthquake_id, set_key):
    earthquake = Earthquake.objects.get(id=earthquake_id)
    Set.objects.create(
        earthquake=earthquake,
        set=get_disaster_set_code(set_key),
        count=0
    )


def create_affection(set_id, grade_key):
    set = Set.objects.get(id=set_id)
    set.count = F('count') + 1
    set.save()
    set.refresh_from_db()
    Affection.objects.create(
        set=set,
        index=get_index_code(set.count),
        grade=get_grade_code(grade_key)
    )


def delete_earthquake(earthquake_id):
    Earthquake.objects.filter(id=earthquake_id).delete()


def delete_set(set_id):
    Set.objects.filter(id=set_id).delete()


def delete_affection(affection_id):
    Affection.objects.filter(id=affection_id).delete()


def retrieve_earthquake(where, when):
    where_code = get_location_code(where)
    when_code = get_time_code(when)
    return Earthquake.objects.filter(Q(where=where_code) & Q(when=when_code))


def retrieve_set(earthquake_id, set_key):
    set_code = get_disaster_set_code(set_key)
    return Set.objects.filter(Q(earthquake=Earthquake.objects.get(id=earthquake_id)) & Q(set=set_code))


def retrieve_affection(set_id):
    return Affection.objects.filter(Q(set=Set.objects.get(id=set_id)))
