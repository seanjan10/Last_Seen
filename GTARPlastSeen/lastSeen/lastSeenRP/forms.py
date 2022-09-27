from django import forms

class createAppearanceForm(forms.Form):
    #clipURL is the video of the character making an appearance, originally made for twitch clips but may be expanded to youtube, facebook and streamable
    clipURL = forms.CharField(label="Twitch clip URL", max_length=125)
    #date and time the character made an appearance, may be adjusted to remove seconds and maybe even minutes as they are not that important
    dateOfAppearance = forms.DateTimeField(widget=forms.DateTimeInput(format=('%Y-%m-%d, %H:%M:%S'),attrs={'class': 'datetimepicker', 'placeholder': 'Select a date', 'type': 'datetime-local'}))
    #dateOfAppearance = forms.CharField(label="Channel of the clip", max_length=30)

    #name of the channel that the clip was created under, may append twitch/facebook/youtube the name that is attached or let the user provide it?
    channelName = forms.CharField(label="Channel of the clip", max_length=30)