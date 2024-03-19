from django import forms
from .models import Person


class RideForm(forms.Form):
  stateSearch = forms.CharField(label='Search', max_length=64, required=False, 
                                widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 200px; margin: 0 auto; display: block;'}))


class NewRideForm(forms.ModelForm):
  class Meta:
    model = Person
    exclude = []
