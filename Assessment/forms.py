
from django import forms
from .models import Outfit
from .models import Evaluacion
from django import forms
from .models import PrendaSuperiorMujer, PrendaInferiorMujer, PrendaCalzadoMujer, PrendaSuperiorHombre, PrendaInferiorHombre
from .models import PrendaCalzadoHombre
class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['imagen']
        


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = [
            'evento', 'lugar', 'tipo_cuerpo'
        ]




class PrendaSuperiorMujerForm(forms.ModelForm):
    class Meta:
        model = PrendaSuperiorMujer
        fields = ['categoria', 'imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'id': 'id_imagen',
                'style': 'display: none;', 
            }),
        }



class PrendaInferiorMujerForm(forms.ModelForm):
    class Meta:
        model = PrendaInferiorMujer
        fields = ['categoria', 'imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'id': 'id_imagen',
                'style': 'display: none;',
            }),
        }
        
class PrendaCalzadoMujerForm(forms.ModelForm):
    class Meta:
        model = PrendaCalzadoMujer
        fields = ['categoria', 'imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'id': 'id_imagen',
                'style': 'display: none;',
            }),
        }


class PrendaSuperiorHombreForm(forms.ModelForm):
    class Meta:
        model = PrendaSuperiorHombre
        fields = ['categoria', 'imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'id': 'id_imagen',
                'style': 'display: none;',
            }),
        }

class PrendaInferiorHombreForm(forms.ModelForm):
    class Meta:
        model = PrendaInferiorHombre
        fields = ['categoria', 'imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'id': 'id_imagen',
                'style': 'display: none;',
            }),
        }
class PrendaCalzadoHombreForm(forms.ModelForm):
    class Meta:
        model = PrendaCalzadoHombre
        fields = ['categoria', 'imagen', 'descripcion']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={
                'id': 'id_imagen',
                'style': 'display: none;',
            }),
        }
