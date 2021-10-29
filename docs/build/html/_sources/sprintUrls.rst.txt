Comentarios
============

from django.conf.urls import url
from django.urls import path
from .views import *
from flujo.views import *

"""
URL para el Sprint crear, listar y modificar
"""
urlpatterns = [
    url(r'^$', SprintListView.as_view(), name='sprint_list'),
    path('create/', view=CreateSprintView.as_view(), name='create_sprint'),
    path('modificar/<int:sprint_pk>/', view=UpdateSprintView.as_view(), name='update_sprint'),
    path('<int:sprint_pk>/asignarus/', view=AsignarUSUpdateView.as_view(), name='asignar_us'),
    path('<int:sprint_pk>/tableros/<int:flujo_pk>/', view=TableroTemplateView.as_view(), name='tablero'),
    path(route='ver/<int:pk>/', view=VerSprintDetailView.as_view(), name='ver_sprint')
    path(route='<int:sprint_pk>/sprintbacklogpdf/', view=SprintBacklogPDF.as_view(), name="reporte_sb"),
    path(route='<int:sprint_pk>/prioridades/', view=PrioridadesPDF.as_view(), name="prioridades")
]
