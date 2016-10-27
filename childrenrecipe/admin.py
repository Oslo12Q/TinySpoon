from django.contrib import admin
from .models import *

# Register your models here.

class MaterialInline(admin.TabularInline):
	model = Material
	extra = 1

class ProcedureInline(admin.TabularInline):
	model = Procedure
	extra = 1

class RecipeAdmin(admin.ModelAdmin):
	filter_horizontal = ('tag',)
	inlines = [
		MaterialInline,
		ProcedureInline,
	]
	list_display = ('id', 'name')
	search_fields = ['name']

class MaterialAdmin(admin.ModelAdmin):
	list_display = ('id','name')
	search_fields = ['name']

class ProcedureAdmin(admin.ModelAdmin):
        search_fields = ['name']

class RecommendAdmin(admin.ModelAdmin):
	raw_id_fields = ('recipe',)
	

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(Procedure,ProcedureAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Recommend,RecommendAdmin)


