from django import forms
from apps.public_services.models import LostAndFound


class LostAndFoundForm(forms.ModelForm):
    class Meta:
        model = LostAndFound
        fields = ['title', 'description', 'categoria', 'contact_info', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do item'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do item'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contato para devolução'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local onde foi perdido/achado'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
