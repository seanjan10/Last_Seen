from django.urls import path, re_path

from . import views


app_name = 'lastSeenRP'
urlpatterns = [
    #homepage
    path('', views.IndexView.as_view(), name='index'),
    #regex pattern since the underscore in the URL things all names except last are part of the first name, since all names other then first are underscored
    re_path(r'^character/(?P<character_FName>([A-Za-z0-9À-ú]|\-|\'|\.)*)_(?P<character_LName>([A-Za-z0-9À-ú]|\-|\'|\.|\_)*)/$', views.character, name='character'),
    #url when the user attempts to submit an appearance into the database
    path('character/<str:character_FName>_<str:character_LName>/resubmit', views.resubmit, name='resubmit'),
]
