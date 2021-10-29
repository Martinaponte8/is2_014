Comentarios
============

from django.urls import path
from django.conf.urls import url

from clientes.views import ProyectosClientePDF
from . import views

"""
Definicion de URLs contenidas en clientes
"""

urlpatterns = [
    url(r'^$', views.ClientListView.as_view(), name='client_list'),
	url(r'^create/$', views.CreateClientView.as_view(), name='create_client'),
	path(route='modificar/<int:pk>/', view=views.UpdateClientView.as_view(), name='update_client'),
	path(route='ver/<int:pk>/', view=views.VerClientDetailView.as_view(), name='ver_cliente'),
	path(route='<int:pk>/reporteclientespdf/', view=ProyectosClientePDF.as_view(), name="reporte_cl")
]