from django import forms
from .models import Configuracion


class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['valor']
        widgets = {
            'valor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'valor'}),
        }
