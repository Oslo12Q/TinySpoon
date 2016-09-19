from django.conf.urls import url, include
from rest_framework import routers
from . import views

from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'category',views.CategoryViewSet)
router.register(r'material',views.MaterialViewSet)
router.register(r'procedure',views.ProcedureViewSet)
router.register(r'recipes',views.RecipeViewSet)
router.register(r'tag',views.TagViewSet)
urlpatterns = [	
        url(r'^', include(router.urls)),
	url(r'^tags$', views.tags, name='tags'),
	url(r'^recipe$',views.recipe, name = 'recipe'),
	url(r'^tagshow$',views.tagshow,name = 'tagshow'),
	
#	url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT },name='static'),

]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
