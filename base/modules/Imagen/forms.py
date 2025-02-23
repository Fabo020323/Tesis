from django import forms

from base.modules.Grupos_Imagenes.models import Grupo
from base.modules.Imagen.models import Imagen


class ImagenForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Seleccione...'}), required=False)

    class Meta:
        model = Imagen
        fields = ['nombre', 'imagen', 'descripcion', 'grupo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion...', 'rows': 3}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['imagen'].required = True
            self.fields['descripcion'].required = True
