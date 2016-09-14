from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from childrenrecipe.serializers import UserSerializer, GroupSerializer
from .models import *
from .serializers import *
from rest_framework.views import APIView

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

	# data = [
	# 	    {
	# 	        "category": "abc",
	# 	        "tags": [
	# 	            {
	# 	                "id": 1,
	# 	                "tag": "bcd"
	# 	            },
	# 	            {
	# 	                "id": 2,
	# 	                "tag": "dce"
	# 	            },
	# 	            {
	# 	                "id": 3,
	# 	                "tag": "cef"
	# 	            }
	# 	        ]
	# 	    }
	# ]
	import pdb
	pdb.set_trace()

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
	
	pdb.set_trace()


	return Response(data, status=status.HTTP_200_OK)














