from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('create/', views.create_story, name='create_story'),
    path('random/', views.random_story, name='random_story'),
    path('<int:story_id>/', views.story_detail, name='story_detail'),
    path('<int:story_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
]