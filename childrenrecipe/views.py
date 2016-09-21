#!/usr/bin/env Python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
from django.utils.timezone import UTC
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
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
        if tags:
                for tag in tags:
                        tag_id = tag.id
                        tag_name = tag.name
                        category_name = tag.category.name
                        category_seq = tag.category.seq
                        categroy = None
                        if category_name in categorys:
                                category = categorys[category_name]
                        else:
                                category = {'seq': category_seq, 'category': category_name, 'tags': []}
                                categorys[category_name] = category
                                data.append(category)
                        category['tags'].append({
                                'id': tag_id,
                                'tag': tag_name,                                                            
                        })

                #import pdb
                #pdb.set_trace()

                if len(data)>1:
                        for item in range(0, len(data)-1):
                                #category_seq = data[item].get('seq')
                                min = item
                                for item2 in range(item+1, len(data)):
                                        if data[item2].get('seq') < data[min].get('seq'):
                                                min = item2
                                tmp = data[item]
                                data[item] = data[min]
                                data[min] = tmp
                        return Response(data, status=status.HTTP_200_OK)
                else:
                        pass

        else:
                return Response(data, status=status.HTTP_404_NOT_FOUND)	

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

@api_view(['GET'])
@permission_classes([AllowAny])
def recommend(request):
        #import pdb 
        #pdb.set_trace()

        now = datetime.datetime.now()
        epoch = datetime.datetime(1970, 1, 1, tzinfo=None).replace(tzinfo=None)
        
	if Recommend.objects.all().filter(pubdate__lte=now): 
                recommend = Recommend.objects.all().filter(pubdate__lte=now).order_by('-pubdate').first()
        
                recommend_image = recommend.image.url
                recommend_pubdate = recommend.pubdate
                recommend_create_time = recommend.create_time
                recommend_recipe_id = recommend.recipe.id
                recommend_recipe_create_time = recommend.recipe.create_time
                recommend_recipe_name = recommend.recipe.name
                recommend_recipe_user = recommend.recipe.user
                recommend_recipe_introduce = recommend.recipe.introduce

		td = recommend_recipe_create_time - epoch
                td1 = recommend_create_time - epoch
                td2 = recommend_pubdate - epoch
		timestamp_recipe_createtime = int(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)
                timestamp_createtime = int(td1.microseconds + (td1.seconds + td1.days * 24 * 3600) * 10**6)
                timestamp_pubdate = int(td2.microseconds + (td2.seconds + td2.days * 24 * 3600) * 10**6)
                
                recommend = {'recommend_recipe': 'Today\'s Specials', 'create_time': timestamp_createtime,
                        'pubdate': timestamp_pubdate, 'image': "http://"+request.META['HTTP_HOST']+recommend_image, 'recipe': {}}

                recommend['recipe'] = {
                        'id': recommend_recipe_id,
                        'create_time': timestamp_recipe_createtime,
                        'name': recommend_recipe_name,
                        'user': recommend_recipe_user,
                        'introduce': recommend_recipe_introduce
                }

                return Response(recommend, status=status.HTTP_200_OK)
        
        else:
                recommend = {}
                return Response(recommend, status=status.HTTP_404_NOT_FOUND)

        
