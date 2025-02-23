from django import forms
from django.contrib.auth.models import Group

from base.modules.usuario.models import CustomUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password', 'placeholder': 'contraseña'}), required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True,
                                   widget=forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    is_active = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input ', 'data-switchery': "true", 'data-plugin': "switchery",
               'data-color': "#039cfd"}))
    class Meta:
        model = CustomUser
        fields = ['username', 'imagen', 'email', 'first_name', 'last_name', 'is_active', 'telefono']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Usuario..'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'correo@gmail.com'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Nombres..'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Apellidos..',
                       'required': 'required'}),
            'telefono': forms.TextInput(
                attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Teléfono..'}),

        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if self.cleaned_data['group']:
                user.groups.clear()
                user.groups.add(self.cleaned_data['group'])
        return user


class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['theme_color_scheme', 'layout_mode', 'layout_width', 'topbar_color', 'menu_color', 'menu_icon',
                  'sidenav_size', 'sidebar_user_info', 'sidenav_twocolumn']
