from django.shortcuts import render
from django_redis import get_redis_connection


def index(request):
    _redis = get_redis_connection("default")
    poem = _redis.get('poem')
    if poem is None:
        poem = _redis.set('poem', 'I v nachale bilo slovo: ')

    args = {
        'poem': poem.decode("utf-8")
    }

    return render(request, 'index.html', args)
