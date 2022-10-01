from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from lastSeenRP.models import rpCharacter, Appearance
from .forms import createAppearanceForm, searchForCharacter, createCharacter
from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.db.models import Q
import pytz


#played by, roleplayed by, portrayed by
#index page that generates a list of all the characters so the user can click on one
class IndexView(generic.ListView):
    #html file to reference
    template_name = 'lastSeenRP/index.html'
    
    #object that is passed into the template
    context_object_name = 'latest_character_list'
    #number of characters per page before pagination
    paginate_by = 203
    #object model that is to be displayed int he list
    model = rpCharacter
    #in which order the list/queryset is to be displayed
    def get_queryset(self):
       return rpCharacter.objects.order_by('character_first_name')[:]
    #get a form object to display the search bar
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["form"] = searchForCharacter()
        return context

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
    #display a new form after attempt
    form = createAppearanceForm(request.POST)
    #if the user attempted to send data by POST
    if request.method == 'POST':
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
            #form = createAppearanceForm()
            #return an error message as they didn't input their data correctly
            return render(request, 'lastSeenRP/character.html', {
                'character_id': character_id,
                'form': form, 
                #'error_message': "Error: you either entered incorrect data or mistyped",  
                })


class searchResults(generic.ListView):
    template_name = 'lastSeenRP/search.html'
    context_object_name = 'search_results_list'
    #paginate_by = 501
    model = rpCharacter()

    #get context variables to be displayed in teh search page, the form and the query the user entered
    def get_context_data(self, **kwargs):
        context = super(searchResults, self).get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("searchQuery")
        context["form"] = searchForCharacter()
        print(type(context))
        return context
    #list of characters that match the search query
    def get_queryset(self):
        query = self.request.GET.get("searchQuery")
        print(query)
        #search fName, nick name, Lname, and streamer name for the user search query, now works for multiple words
        search_results_list = rpCharacter.objects.all()
        for term in query.split():

            search_results_list = search_results_list.filter(
            Q(character_first_name__icontains=term) 
            | Q(character_nick_name__icontains=term) 
            | Q(character_last_name__icontains=term) 
            | Q(character_played_by__icontains=term)
            )
        return search_results_list

class createCharacterEntry(generic.FormView):
    template_name = 'lastSeenRP/create.html'
    form_class = createCharacter

    #make validation function, error message if exists

    #invalid if the user submits a user that is already defined in the database
    def form_invalid(self, form):
        #print(form.cleaned_data['character_first_name'])
        try: 
            fName = form.cleaned_data['character_first_name']
        except KeyError:
           # messages.error(self.request, "First names cannot include spaces. Additional names should be added into the last name box. Characters that are allowed are (-, ', .)")
            return super(createCharacterEntry, self).form_invalid(form)
        lName = form.cleaned_data['character_last_name']
        
        if rpCharacter.objects.filter(character_first_name=fName, character_last_name=lName).exists():
            messages.error(self.request, "ERROR: You can not submit a character that is already in the database.")
        return super(createCharacterEntry, self).form_invalid(form)

    #save the character object
    def form_valid(self, form):
        
        character= form.save()
        self.character_first_name = character.character_first_name
        self.character_last_name = character.character_last_name
        messages.success(self.request, "Successfully inserted character into the database")

        return super(createCharacterEntry, self).form_valid(form)

    #if the data is valid redirects to the newly created page of the user submitted data
    def get_success_url(self):
        return reverse('lastSeenRP:character', kwargs={'character_FName': self.character_first_name, 'character_LName': self.character_last_name})
    
    
