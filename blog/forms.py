from django import forms
from .models import Comentario

# Formulario personalizado . Los campos del formulario son creados manualmente.
class EmailPostForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    email = forms.EmailField()
    para = forms.EmailField()
    comentarios = forms.CharField(required=False, widget=forms.Textarea)
    
# Formulario basado en el modelo Comment
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'email', 'cuerpo'] # Campos que se mostrarán en el formulario