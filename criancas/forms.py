from django import forms
from .models import Crianca

class CriancaForm(forms.ModelForm):
    class Meta:
        model = Crianca
        fields = ['nome', 'data_nascimento', 'foto']
        labels = {
            'nome': 'Nome completo',
            'data_nascimento': 'Data de nascimento',
            'foto': 'Foto (opcional)',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Maria Souza',
                'autofocus': True,
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }