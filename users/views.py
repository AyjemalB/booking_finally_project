from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated



@api_view(['POST', 'GET'])
def register_view(request):
    if request.method == 'GET':
        return Response({'message': 'Login endpoint is working. Use POST to log in.'})
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email и пароль обязательны'}, status=400)

    user = authenticate(request, email=email, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Неверные данные'}, status=401)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [AllowAny] # <- временно отключает проверку
    permission_classes = [IsAuthenticated]