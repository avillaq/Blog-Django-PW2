from django import forms
from .models import Comentario
    
# Formulario basado en el modelo Comment
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'email', 'cuerpo'] # Campos que se mostrarán en el formulario