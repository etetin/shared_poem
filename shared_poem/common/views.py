from django.shortcuts import render
from django_redis import get_redis_connection


def index(request):
    _redis = get_redis_connection("default")
    poem = _redis.get('poem').decode("utf-8")
    args = {
        'poem': poem
    }

    return render(request, 'index.html', args)
