from django.urls import path, re_path

from . import views


app_name = 'lastSeenRP'
urlpatterns = [
    #homepage
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    #each charcters page
    #path('character/<str:character_FName>__<str:character_LName>/', views.character, name='character'),
    re_path(r'^character/(?P<character_FName>([A-Za-z0-9À-ú]|\-|\'|\.)*)_(?P<character_LName>([A-Za-z0-9À-ú]|\-|\'|\.|\_)*)/$', views.character, name='character'),
    #path('character/<str:character_FName>_<str:character_LName>/', views.CharacterFormView.as_view(), name='character'),
    path('character/<str:character_FName>_<str:character_LName>/resubmit', views.resubmit, name='resubmit'),
    #path('character/<str:character_name>/', views.character, name='character'),
    #path('character/<int:character_id>/', views.character, name='character'),
   # path('character/<str:character_FName>_<str:character_LName>/create_appearance/<int:ap_id>/', views.appearanceOfCharacter, name='appearanceOfCharacter'),
    #path('appearance/create/<int:ap_id>/', views.createAppearance, name='createAppearance')
]
