from django import forms
from .models import Comment

# Formulario personalizado . Los campos del formulario son creados manualmente.
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
# Formulario basado en el modelo Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body'] # Campos que se mostrarán en el formulario