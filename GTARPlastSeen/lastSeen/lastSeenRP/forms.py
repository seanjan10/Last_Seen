from django import forms
from lastSeenRP.models import rpCharacter
from lastSeenRP.validators import *

class createAppearanceForm(forms.Form):
    #clipURL is the video of the character making an appearance, originally made for twitch clips but may be expanded to youtube, facebook and streamable
    clipURL = forms.CharField(label="Twitch clip URL", validators=[validate_clip_url], max_length=125)
    #date and time the character made an appearance, may be adjusted to remove seconds and maybe even minutes as they are not that important
    dateOfAppearance = forms.DateTimeField(label="Date of Appearance", validators=[validate_appearance_time], widget=forms.DateTimeInput(format=('%Y-%m-%d, %H:%M:%S'),attrs={'class': 'datetimepicker', 'placeholder': 'Select a date', 'type': 'datetime-local'}))
    #dateOfAppearance = forms.CharField(label="Channel of the clip", max_length=30)

    #name of the channel that the clip was created under, may append twitch/facebook/youtube the name that is attached or let the user provide it?
    channelName = forms.CharField(label="Channel of the clip",  max_length=30)


class searchForCharacter(forms.Form):
    searchQuery = forms.CharField(label="Search", max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Search', 'class':'form-control mr-sm-2', 'type':'search', 'aria-label':'Search'}))

class createCharacter(forms.ModelForm):

    class Meta:
        model = rpCharacter
        fields = [
        'character_first_name', 
        'character_nick_name', 
        'character_last_name',
        'character_played_by',
        'character_image',
        'streamers_URL' ]

        widgets= {
            'character_first_name': forms.TextInput(attrs={'placeholder': 'Character First Name'}), 
            'character_nick_name': forms.TextInput(attrs={'placeholder': 'Character Nick Name'}),
            'character_last_name': forms.TextInput(attrs={'placeholder': 'Character Last Name'}),
            'character_played_by': forms.TextInput(attrs={'placeholder': 'Username of the player'}),
            'character_image': forms.TextInput(attrs={'placeholder': 'Image URL of character'}),
            'streamers_URL': forms.TextInput(attrs={'placeholder': 'URL of the players stream'})
            
        }
