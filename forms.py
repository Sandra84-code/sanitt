from django import forms

from .models import Compound
from .models import Target

class CompoundForm(forms.Form):
    compoundsearch = forms.CharField(label='Enter name', max_length=100)

class TargetForm(forms.Form):
    tsearch = forms.CharField(label='Enter name', max_length=100)
