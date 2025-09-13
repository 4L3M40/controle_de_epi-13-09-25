from django import forms
from .models import Epi

class EpiForm(forms.ModelForm):
    class Meta:
        model = Epi
        fields = '__all__'