from django.conf.urls import url
from django.urls import path
from . import views
from .views import eliminar2
#from tipoUserStory.views import *
#from userstory.views import *
#from sprint.views import *

"""
Definicion de URLs contenidas en proyectos
"""

urlpatterns = [

    #administracion

    url(r'^$', views.ProjectListView.as_view(),name='project_list'),
	url(r'^create/$', views.CreateProjectView.as_view(), name='create_project'),
    path(route='update_project/<int:pk_proyecto>/', view=views.UpdateProjectView.as_view(), name='update_project'),
    path("eliminar/<int:project_id>/", eliminar2, name="eliminar2"),
    #definicion

    url(r'^opciones/$', views.OptionsListView.as_view(), name='options_project'),
    path(route='opciones/<int:pk_proyecto>/', view=views.UpdateOptionsView.as_view(), name='update_options'),
    path(route='opciones/<int:pk_proyecto>/flujos/create/', view=views.CreateFlujoView.as_view(), name='create_options_flujo'),
    path(route='opciones/<int:pk_proyecto>/flujos/<int:pk>/', view=views.UpdateFlujoView.as_view(), name='update_options_flujo'),
    path(route='opciones/<int:pk_proyecto>/flujos/', view=views.FlujoListView.as_view(), name='update_options_flujo_list'),
    #path(route='opciones/<int:pk_proyecto>/tipoUserStory/', view=tipoUserStoryListView.as_view(), name='user_story_type_list'),
    #path(route='opciones/<int:pk_proyecto>/tipoUserStory/create/', view=CreateUserStoryTypeView.as_view(), name='create_user_story_type'),
	#path(route='opciones/<int:pk_proyecto>/tipoUserStory/<int:pk>/', view=UpdateUserStoryTypeView.as_view(), name='update_user_story_type'),
    path(route='opciones/<int:pk_proyecto>/asignarRoles/', view=views.UpdateDetalleProyectoView.as_view(), name='update_roles_proyecto'),

    #ejecucion

    url(r'^ejecuciones/$', views.EjecucionListView.as_view(), name='options_project'),
    path(route='ejecuciones/<int:pk_proyecto>/', view=views.UpdateEjecucionView.as_view(), name='update_ejecucion'),
    #path(route='ejecuciones/<int:pk_proyecto>/userstory/', view=UserStoryListView.as_view(), name='user_story_list'),
    #path(route='ejecuciones/<int:pk_proyecto>/userstory/create/', view=CreateUserStoryView.as_view(), name='create_userstory'),
	#path(route='ejecuciones/<int:pk_proyecto>/userstory/<int:pk>/', view=UpdateUserStoryView.as_view(), name='update_userstory'),
    #path(route='ejecuciones/<int:pk_proyecto>/productbacklog/',view=ProductBacklogListView.as_view(), name = 'product_backlog'),
    #path(route='ejecuciones/<int:pk_proyecto>/sprint/', view=SprintListView.as_view(), name='sprint_list'),
    #path(route='ejecuciones/<int:pk_proyecto>/sprint/create/', view=CreateSprintView.as_view(), name='create_sprint'),
	#path(route='ejecuciones/<int:pk_proyecto>/sprint/<int:pk>/', view=UpdateSprintView.as_view(), name='update_sprint'),
]
