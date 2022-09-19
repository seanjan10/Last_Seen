from django import forms

class createAppearanceForm(forms.Form):
    clipURL = forms.CharField(label="Twitch clip URL", max_length=125)
    dateOfAppearance = forms.DateTimeField(widget=forms.DateTimeInput(format=('%Y-%m-%d, %H:%M:%S'),attrs={'class': 'datetimepicker', 'placeholder': 'Select a date', 'type': 'datetime-local'}))
    #dateOfAppearance = forms.CharField(label="Channel of the clip", max_length=30)
    channelName = forms.CharField(label="Channel of the clip", max_length=30)