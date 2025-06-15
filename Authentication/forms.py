from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'genero', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'genero': 'Género',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email').split('@')[0] + str(CustomUser.objects.count())
        if commit:
            user.save()
        return user
