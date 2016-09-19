#!/usr/bin/env Python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from childrenrecipe.serializers import *
from .models import *
from .serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)
from rest_framework.decorators import (
	api_view,
	permission_classes,
	parser_classes,
)
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

        queryset = Group.objects.all()
        serializer_class = GroupSerializer

class APIRootView(APIView):
    def get(self, request):
        year = now().year
        data = {

            'year-summary-url': reverse('year-summary', args=[year], request=request)
        }
        return Response(data)

class RecipeViewSet(viewsets.ModelViewSet):
	queryset = Recipe.objects.all()
#	serializer_class_create = RecipeCreateSerializer
	serializer_class = RecipeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class MaterialViewSet(viewsets.ModelViewSet):
	queryset = Material.objects.all()
	serializer_class = MaterialSerializer

class ProcedureViewSet(viewsets.ModelViewSet):
	queryset = Procedure.objects.all()
	serializer_class = ProcedureSerializer

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def tags(request):
	data = []
	categorys = {}
	tags = Tag.objects.all()
	for tag in tags:
		tag_id = tag.id
		tag_name = tag.name
		category_name = tag.category.name
		categroy = None
		if category_name in categorys:
			category = categorys[category_name]
		else:
			category = {'category': category_name, 'tags': []}
			categorys[category_name] = category
			data.append(category)
		category['tags'].append({
			'id': tag_id,
			'tag': tag_name
		})
	return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def recipes(request):
	
	data = []
	tag ={'recipes': []}
	month = request.GET.get('month',None)
	limit = request.GET.get('limit',None)
	recipes = Recipe.objects.filter(tag__name=month)
	if recipes is None:
		raise BadRequestException(detail='Recipes not found')
	else:
		for recipe in recipes:
			import pprint
			pprint.pprint(recipe_exihibitpic)
			recipe_id = recipe.id
			recipe_create_time = recipe.create_time
			recipe_name = recipe.name
			recipe_user = recipe.user
			recipe_exihibitpic = recipe.exihibitpic
			recipe_introduce = recipe.introduce
			tag_name=recipe.tag.values()[0]
			tag['recipes'].append({
				'id':recipe_id,
				'create_time':recipe_create_time,
				'recipe':recipe_name,
				'user':recipe_user,
                'exihibitpic': recipe_exihibitpic.url,
				#'exihibitpic':"http://"+request.META['HTTP_HOST']+'/'+'api'+'/'+'recipes'+'/'+recipe_exihibitpic.url,
				'introduce':recipe_introduce,
				'tag':tag_name
			})
		data.append(tag)
		return Response(data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def recipesshow(request): 
        data = []
        tag ={'recipes': []}
        recipes = Recipe.objects.all()
        for recipe in recipes:
                recipe_id = recipe.id
                recipe_create_time = recipe.create_time
                recipe_name = recipe.name
                recipe_user = recipe.user
                recipe_exihibitpic = recipe.exihibitpic
                recipe_introduce = recipe.introduce
                tag_name=recipe.tag.values()[0]
                tag['recipes'].append({
                        'id':recipe_id,
                        'create_time':recipe_create_time,
                        'recipe':recipe_name,
                        'user':recipe_user,
                        'exihibitpic':"http://"+request.META['HTTP_HOST']+'/'+'api'+'/'+'recipes'+'/'+recipe_exihibitpic.url,
                        'introduce':recipe_introduce,
			'tag':tag_name
                })
	data.append(tag)
        return Response(data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def tagshow(request):
	data = []
        categorys = {}
        tags = Tag.objects.filter(category_id='1')
        for tag in tags:
                tag_id = tag.id
                tag_name = tag.name
                category_name = tag.category.name
                categroy = None
                if category_name in categorys:
                        category = categorys[category_name]
                else:
                        category = {'category': category_name, 'tags': []}
                        categorys[category_name] = category
                        data.append(category)
                category['tags'].append({
                        'id': tag_id,
                        'tag': tag_name
                })
        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_search(request):	
	recipe_name = request.GET.get('recipe_name',None)
	recipes = Recipe.objects.filter(name = recipe_name)
	data = []
        tag ={'recipes': []}
        for recipe in recipes:
                recipe_id = recipe.id
                recipe_create_time = recipe.create_time
                recipe_name = recipe.name
                recipe_user = recipe.user
                recipe_exihibitpic = recipe.exihibitpic
                recipe_introduce = recipe.introduce
                tag_name=recipe.tag.values()[0]
                tag['recipes'].append({
                        'id':recipe_id,
                        'create_time':recipe_create_time,
                        'recipe':recipe_name,
                        'user':recipe_user,
                        'exihibitpic':"http://"+request.META['HTTP_HOST']+'/'+'api'+'/'+'recipes'+'/'+recipe_exihibitpic.url,
                        'introduce':recipe_introduce,
                        'tag':tag_name
                })
        data.append(tag)
        return Response(data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_filter_search(request):
	
        data = []
        tag ={'recipes': []}
        month = request.GET.get('month',None)
        limit = request.GET.get('limit',None)
        recipes = Recipe.objects.filter(tag__name=month)
        if recipes is None:
                raise BadRequestException(detail='Recipes not found')
        else:
                for recipe in recipes:
                        recipe_id = recipe.id
                        recipe_create_time = recipe.create_time
                        recipe_name = recipe.name
                        recipe_user = recipe.user
                        recipe_exihibitpic = recipe.exihibitpic
                        recipe_introduce = recipe.introduce
                        tag_name=recipe.tag.values()[0]
                        tag['recipes'].append({
                                'id':recipe_id,
                                'create_time':recipe_create_time,
                                'recipe':recipe_name,
                                'user':recipe_user,
                                'exihibitpic':"http://"+request.META['HTTP_HOST']+'/'+'api'+'/'+'recipes'+'/'+recipe_exihibitpic.url,
                                'introduce':recipe_introduce,
                                'tag':tag_name
                        })
                data.append(tag)
                return Response(data,status=status.HTTP_200_OK)

