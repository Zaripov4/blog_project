from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterUser
from .models import News


@api_view(["POST"])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    __, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token
    })


@api_view(["GET"])
def get_data(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_info':
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
        })
    return Response({'error': 'not authenticated'}, status=400)


@api_view(["POST"])
def register(request):
    serializer = RegisterUser(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    __, token = AuthToken.objects.create(user)
    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'token': token
    })


def news(request):
    title = News.title
    body = News.body
    category = News.category
    picture = News.picture

    return title
