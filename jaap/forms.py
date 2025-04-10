from django import forms
from .models import JaapSession

class JaapInputForm(forms.Form):
    """
    Form for Ram Naam Jaap input
    """
    jaap_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'jaap-input w-full',
                'placeholder': 'Type Ram here...',
                'x-model': 'jaapText',
                'x-on:keyup': 'processInput',
                'autofocus': 'autofocus',
                'rows': '8'
            }
        ),
        required=False
    )
    
    timer = forms.ChoiceField(
        choices=[
            ('', 'No Timer'),
            ('5', '5 Minutes'),
            ('10', '10 Minutes'),
            ('15', '15 Minutes'),
            ('30', '30 Minutes'),
            ('60', '60 Minutes'),
        ],
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'hidden',
                'x-model': 'selectedTimer'
            }
        )
    )
    
    target = forms.ChoiceField(
        choices=[
            ('', 'No Target'),
            ('108', '108 Times'),
            ('1008', '1,008 Times'),
            ('10000', '10,000 Times'),
            ('100000', '100,000 Times'),
        ],
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'hidden',
                'x-model': 'selectedTarget'
            }
        )
    )
    
    session_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'x-model': 'sessionId'
            }
        )
    )
    
    ram_count = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'x-model': 'ramCount'
            }
        )
    )

class JaapSessionForm(forms.ModelForm):
    """
    Form for managing Jaap sessions
    """
    class Meta:
        model = JaapSession
        fields = ['timer_set', 'target_count', 'status']
        widgets = {
            'timer_set': forms.Select(
                attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent'}
            ),
            'target_count': forms.NumberInput(
                attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent'}
            ),
            'status': forms.Select(
                attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent'}
            ),
        } 