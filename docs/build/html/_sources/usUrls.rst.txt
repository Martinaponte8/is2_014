Comentarios
============

from django.conf.urls import url
from django.urls import path
from .views import UpdateUserStoryView, VerUserStoryDetailView, CreateUserStoryView, UserStoryListView, eliminar4

"""
URL para el tipo de User Story, crear, listar y modificar
"""
urlpatterns = [
    url(r'^$', UserStoryListView.as_view(), name='user_story_list'),
    path('create/', view=CreateUserStoryView.as_view(), name='create_userstory'),
    path('modificar/<int:pk>/', view=UpdateUserStoryView.as_view(), name='update_userstory'),
    path(route='ver/<int:pk>/', view=VerUserStoryDetailView.as_view(), name='ver_userstory'),
    path('eliminar/<int:us_id>/', eliminar4, name="eliminar4")
]