
from django.conf.urls import url
from django.urls import path
from . import views
from .views import eliminar3
# from django.contrib.auth.views import login
from .models import *

"""
URL para el ver, crear y modificar roles
"""

urlpatterns = [
	url(r'^$', views.RolListView.as_view(),name='rol_list'),
	url(r'^create/$', views.CreateRolView.as_view(), name='create_rol'),
	path(route='update_rol/<int:pk>/', view=views.UpdateRolView.as_view(), name='update_rol'),
	path("eliminar/<int:rol_id>/", eliminar3, name="eliminar3"),
]