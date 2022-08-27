from django.urls import path

from . import views


app_name = 'lastSeenRP'
urlpatterns = [
    #homepage
    path('', views.index, name='index'),
    #each charcters page
    path('character/<str:character_FName>_<str:character_LName>/', views.character, name='character'),
    #path('character/<str:character_name>/', views.character, name='character'),
    #path('character/<int:character_id>/', views.character, name='character'),
    path('appearance/<int:ap_id>/', views.appearanceOfCharacter, name='appearanceOfCharacter')
]
