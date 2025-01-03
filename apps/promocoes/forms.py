from django import forms
from apps.promocoes.models import Promocao, ImagemPromocao


class PromocaoForm(forms.ModelForm):
    class Meta:
        model = Promocao
        fields = ['empresa', 'titulo', 'descricao', 'imagem_principal', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem_principal': forms.FileInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-control'}),
        }

class ImagemPromocaoForm(forms.ModelForm):
    class Meta:
        model = ImagemPromocao
        fields = ['imagem', 'legenda']
        widgets = {
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'legenda': forms.TextInput(attrs={'class': 'form-control'}),
        }
