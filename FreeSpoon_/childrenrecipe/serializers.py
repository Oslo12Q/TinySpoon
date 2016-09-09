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

class CategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Category
		fields = ('url','name')

class TagSerializer(serializers.HyperlinkedModelSerializer):
	category_name = serializers.CharField(source='category.name')
	class Meta:
		model = Tag
		fields = ('name','category_name')

class MaterialSerializer(serializers.HyperlinkedModelSerializer):
        recipe_title = serializers.CharField(source='recipe.name')
        class Meta:
                model = Material
                fields = ('url','id','recipe_title','name','quantity','measureunits')   

class ProcedureSerializer(serializers.HyperlinkedModelSerializer):
        recipe = serializers.CharField(source='recipe.name')
        class Meta:
                model = Procedure
                fields = ('url','id','recipe','seq','describe','image')

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
	tag = TagSerializer(many=True)
	material = MaterialSerializer(source='material_set',many=True)
	procedure = ProcedureSerializer(source='procedure_set',many=True)
        class Meta:
                model = Recipe
                fields = ('url','id','name','user','exihibitpic','introduce','tag',
			'material','procedure'
			)


