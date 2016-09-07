from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt
import pdb

class UserSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = User
            fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Group
            fields = ('url', 'name')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Student
            fields = ('url','name','age','sax')

class ClassesSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Classes
            fields = ('student','classname')


class ClassesCreateSerializer(serializers.Serializer):
        classname = serializers.CharField(allow_blank=True)
        student = serializers.ListField(
                child = serializers.IntegerField()
        )
        def create(self,validated_data):
                pdb.set_status()
                classname = validated_data.get('classname')
                student = validated_data.get('studebt')
                try:
                        classname = validated_data.get('classname')

                        classes = Classes.objects.create(
                                classname=classname
                        )
                        classes.objects.create(student=student)
                        return classes
                except IntegrityError:
                        raise BadRequestException(detail='Create failed')

