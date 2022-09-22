from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from lastSeenRP.models import rpCharacter, Appearance
from .forms import createAppearanceForm
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.views import generic
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'lastSeenRP/index.html'
    context_object_name = 'latest_character_list'

    def get_queryset(self):
       return rpCharacter.objects.order_by('-character_first_name')[:10]
       
    



#def index(request):
    
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
'''
    latest_character_list = rpCharacter.objects.order_by('-character_first_name')[:5]
    context = {'latest_character_list': latest_character_list}
    return render(request, 'lastSeenRP/index.html', context)

'''
'''
class CharacterFormView(generic.FormView):
    template_name = 'lastSeenRP\character.html'
    form_class = createAppearanceForm
    success_url = '/lastSeenRP/character/'
'''
    

def character(request, character_FName, character_LName):
    form = createAppearanceForm()

    character_id = get_object_or_404(rpCharacter, character_first_name=character_FName, character_last_name=character_LName)
    return render(request, 'lastSeenRP/character.html', {'character_id': character_id, 'form':form})
    
    '''
    try:
        character_id = rpCharacter.objects.get(character_first_name=charFirstName, character_last_name=charLastName)
    except rpCharacter.DoesNotExist:
        raise Http404("This Character does not exist or has not been added to the Database yet")
    return render(request, 'lastSeenRP/character.html', {'character_id': character_id})
    '''

def appearanceOfCharacter(request, character_FName, character_LName):
    response = "you're looking at the appearance %s"
    return HttpResponse(response % character_FName)


def resubmit(request, character_FName, character_LName):
    character_id = get_object_or_404(rpCharacter, character_first_name=character_FName, character_last_name=character_LName)
    if request.method == 'POST':
        form = createAppearanceForm(request.POST)
        print(character_id)
        
        if form.is_valid():
            u = form.cleaned_data["clipURL"]
            d = form.cleaned_data["dateOfAppearance"]
            c = form.cleaned_data["channelName"]
            a = Appearance(character_name=character_id, twitch_clip_URL=u, date_of_appearance=d, clip_Streamer=c, publish_time=datetime.now())
            a.save()
            #return render(request, 'lastSeenRP/character.html', {'character_id': character_id, 'form':form})
            messages.success(request, 'Successfully submitted an appearance!')
            return HttpResponseRedirect(reverse('lastSeenRP:character', args=(character_FName, character_LName,)))
        else:
            #print('is it reaching this uhoh this might be bad')
            form = createAppearanceForm()
            return render(request, 'lastSeenRP/character.html', {
                'character_id': character_id,
                'form': form, 
                'error_message': "Error: you either entered incorrect data or mistyped",  
                })
