from rest_framework import generics
from rest_framework.response import Response
from account.serializers import RegisterSerializer, UserSerializer


class RegisterApi(generics.GenericAPIView):
    queryset = RegisterSerializer.data
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer()).data,
            'message':
                'User created successfully. '
                'Now perform Login to get your token',
        })
