from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework import generics, permissions
from rest_framework.response import Response
from accounts.serializers import UserSerializer, RegisterSerializer,UserSalarySerializer,LoginSerializer
from accounts.models import User
from django.db.models import Sum
from django.contrib import auth
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.




class RegisterAPI(generics.GenericAPIView):
    ''' Register API '''
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data={
            'response':'Successfully registered a new user.',
            'email': user.email,
            'username':user.username,
        }
        return Response(data)



class LoginView(generics.GenericAPIView): 
    serializer_class = LoginSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY)

            serializer = LoginSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]


class SalaryList(ListAPIView):
    queryset = User.objects.values('department').annotate(total_count= Sum('salary'))
    serializer_class = UserSalarySerializer 
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSalarySerializer(queryset, many=True)
        data = {
            'data':queryset
        }
        return Response(data)