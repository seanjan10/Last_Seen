from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from lastSeenRP.models import rpCharacter
# Create your views here.

def index(request):
    
    #return HttpResponse("Hello world, you are at the lastSeen Index.")
    '''latest_character_list = rpCharacter.objects.order_by('-character_first_name')[:5]
    output = ','.join([c.character_played_by for c in latest_character_list])
    return HttpResponse(output) '''

    #latest_character_list = rpCharacter.objects.order_by('-character_first_name')[:5]
    '''template = loader.get_template('lastSeenRP/index.html')
    context = {
        'latest_character_list' : latest_character_list,
    }
    return HttpResponse(template.render(context, request))'''

    latest_character_list = rpCharacter.objects.order_by('-character_first_name')[:5]
    context = {'latest_character_list': latest_character_list}
    return render(request, 'lastSeenRP/index.html', context)


def character(request, character_FName, character_LName):
    '''response = "You're looking at character %s"
    return HttpResponse(response % character_name)'''
    
    character_id = get_object_or_404(rpCharacter, character_first_name=character_FName, character_last_name=character_LName)
    return render(request, 'lastSeenRP/character.html', {'character_id': character_id})

    '''
    try:
        character_id = rpCharacter.objects.get(character_first_name=charFirstName, character_last_name=charLastName)
    except rpCharacter.DoesNotExist:
        raise Http404("This Character does not exist or has not been added to the Database yet")
    return render(request, 'lastSeenRP/character.html', {'character_id': character_id})
    '''

def appearanceOfCharacter(request, ap_id):
    response = "you're looking at the appearance %s"
    return HttpResponse(response % ap_id)

