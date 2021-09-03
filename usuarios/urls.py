from django.conf.urls import url
from django.urls import path
#from django import forms
#from usuarios import views
#
from . import views
from .views import eliminar

"""
URL para Usuarios: crear, listar, modificar y eliminar
"""

urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'), url(r'^create/$', views.CreateUserView.as_view(), name='create_user'),
    path(route='update_user/<int:pk>/', view=views.UpdateUserView.as_view(), name='update_user'),
    #path(route='update_user/<int:user_id>/', view=views.eliminar(), name='eliminar')
    path("eliminar/<int:user_id>/", eliminar, name="eliminar"),
]
