from django.conf.urls import include, url
from django.urls import path
# from proyecto import views
from . import views
from proyecto.views import eliminar2
from userstory.views import *
# from .views import eliminar2
#from tipoUserStory.views import *
#from userstory.views import *
from sprint.views import *

"""
Definicion de URLs contenidas en proyectos
"""

urlpatterns = [

    #administracion

    url(r'^$', views.ProjectListView.as_view(), name='project_list'),
    url(r'^create/$', views.CreateProjectView.as_view(), name='create_project'),
    path(route='update_project/<int:pk_proyecto>/', view=views.UpdateProjectView.as_view(), name='update_project'),
    path("eliminar/<int:project_id>/", eliminar2, name="eliminar2"),
    #definicion

    url(r'^opciones/$', views.OptionsListView.as_view(), name='options_project'),
    path(route='opciones/<int:pk_proyecto>/', view=views.UpdateOptionsView.as_view(), name='update_options'),
    path('opciones/<int:pk_proyecto>/flujos/', include('flujo.urls')),
    path('opciones/<int:pk_proyecto>/tipoUserStory/', include('tipoUserStory.urls'), name='user_story_type_list'),
    path(route='opciones/<int:pk_proyecto>/asignarRoles/', view=views.UpdateTeamMemberView.as_view(), name='update_roles_proyecto'),

    #ejecucion

    url(r'^ejecuciones/$', views.EjecucionListView.as_view(), name='options_project'),
    path(route='ejecuciones/<int:pk_proyecto>/', view=views.UpdateEjecucionView.as_view(), name='update_ejecucion'),
    path('ejecuciones/<int:pk_proyecto>/userstory/', include('userstory.urls')),
    path(route='ejecuciones/<int:pk_proyecto>/productbacklog/', view=ProductBacklogListView.as_view(), name='product_backlog'),
    path('ejecuciones/<int:pk_proyecto>/sprint/', include('sprint.urls')),
    path(route='ver/<int:pk>/', view=views.VerProyectoDetailView.as_view(), name='ver_project'),
    path(route='ejecuciones/<int:pk_proyecto>/productbacklogpdf/', view=ProductBacklogPDF.as_view(), name="reporte_pb"),
    path(route='ejecuciones/<int:pk_proyecto>/horastrabajadas/', view=views.HorasTrabajadasPDF.as_view(),name="horas_trabajadas")
]

