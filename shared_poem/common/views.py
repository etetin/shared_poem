from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    _redis = get_redis_connection("default")
    poem = _redis.get('poem')
    args = {
        'poem': poem
    }

    return render(request, 'index.html', args)


@api_view(['POST', ])
def add_symbol(request):
    print(request.data['symbol'])

    return Response()
