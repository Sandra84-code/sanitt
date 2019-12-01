from django import forms

class CompoundForm(forms.Form):
    compound_name = forms.CharField(label='Enter name', max_length=100)
