from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from childrenrecipe.serializers import UserSerializer, GroupSerializer
from .models import *
from .serializers import StudentSerializer, ClassesSerializer,ClassesCreateSerializer
from rest_framework.views import APIView
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

        queryset = Group.objects.all()
        serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):

        queryset = Student.objects.all()
        serializer_class = StudentSerializer


class ClassViewSet(viewsets.ModelViewSet):

        queryset = Classes.objects.all()

        serializer_class = ClassesSerializer
        serializer_class_create = ClassesCreateSerializer

class APIRootView(APIView):
    def get(self, request):
        year = now().year
        data = {

            'year-summary-url': reverse('year-summary', args=[year], request=request)
        }
        return Response(data)

