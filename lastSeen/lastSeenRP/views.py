from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from lastSeenRP.models import rpCharacter, Appearance
from .forms import createAppearanceForm
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.views import generic
import pytz


#played by, roleplayed by, portrayed by
#index page that generates a list of all the characters so the user can click on one
class IndexView(generic.ListView):
    #html file to reference
    template_name = 'lastSeenRP/index.html'
    #object that is passed into the template
    context_object_name = 'latest_character_list'
    #number of characters per page before pagination
    paginate_by = 501
    #object model that is to be displayed int he list
    model = rpCharacter
    #in which order the list/queryset is to be displayed
    def get_queryset(self):
       return rpCharacter.objects.order_by('character_first_name')[:]
       
    



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

#view to display the characters page with a list of all their appearances
def character(request, character_FName, character_LName):
    #form context objects to be passed into the template
    form = createAppearanceForm()

    #print(character_FName)
    #print(character_LName)

    #retrieve specific object that is refered to by the first and last name
    character_id = get_object_or_404(rpCharacter, character_first_name=character_FName, character_last_name=character_LName)

    #print(character_id)
    #render the template with context variables to be displayed to the user
    return render(request, 'lastSeenRP/character.html', {'character_id': character_id, 'form':form})

#view to display when the user attempts to enter an appearance under a character
def resubmit(request, character_FName, character_LName):
    #retrieve the id of the character based off the first and last name
    character_id = get_object_or_404(rpCharacter, character_first_name=character_FName, character_last_name=character_LName)
    #if the user attempted to send data by POST
    if request.method == 'POST':
        #display a new form after attempt
        form = createAppearanceForm(request.POST)
        #print(character_id)
        
        #if the data entered passes validation checks
        if form.is_valid():
            #retrieve data from the form and use it to create an Appearance
            u = form.cleaned_data["clipURL"]
            d = form.cleaned_data["dateOfAppearance"]
            c = form.cleaned_data["channelName"]
            #as of now, time is stored in UTC time
            a = Appearance(character_name=character_id, twitch_clip_URL=u, date_of_appearance=d, clip_Streamer=c, publish_time=pytz.UTC.localize(datetime.now()))
            #enter record into the Database
            a.save()
            #display success message to user
            messages.success(request, 'Successfully submitted an appearance!')
            #send user back to the character view as they their entry was successful, redirect so data isn't accidentally entered twice
            return HttpResponseRedirect(reverse('lastSeenRP:character', args=(character_FName, character_LName,)))
        #if the data entered did not pass validation checks 
        else:
            #create a new form
            form = createAppearanceForm()
            #return an error message as they didn't input their data correctly
            return render(request, 'lastSeenRP/character.html', {
                'character_id': character_id,
                'form': form, 
                'error_message': "Error: you either entered incorrect data or mistyped",  
                })
