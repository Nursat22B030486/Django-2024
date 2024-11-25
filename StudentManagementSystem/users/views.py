from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .models import User
from .serializers import UserSignUpSerializer, UserSerializer
from .permissions import IsAdmin
from students.models import Student

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAdmin]) 
def signup(request):

    data = request.data
    serializer = UserSignUpSerializer(data=data)

    if serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password']),
                role=data.get('role', 'Student')
            )
            user.save()

            if user.role == 'Student':
                Student.objects.create(user=user, name=user.username, email=user.email,)
            return Response({'message': 'User Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

