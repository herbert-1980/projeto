from django import forms
from . import models
from django.forms import inlineformset_factory
from apps.banners.models import Banner, BannerImage


class BannerForm(forms.ModelForm):

    class Meta:
        model = models.Banner
        fields = ['fantasia', 'banner', 'destaque', 'data_inicio', 'data_final',  'categorias', 'letra']
        widgets = {
            'fantasia': forms.Select(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'destaque': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_final': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'letra': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'fantasia': 'Nome da Empresa',
            'banner': 'Banner',
            'destaque': 'Destaque',
            'data_inicio': 'Data Inicial',
            'data_final': 'Data Final',
            'categorias': 'Categoria',
            'letra': 'Letra',
        }
# Formset para imagens adicionais
BannerImageFormSet = inlineformset_factory(
    Banner,
    BannerImage,
    fields=['additional_images'],
    extra=3,  # Número de campos extras para imagens adicionais
    widgets={
        'additional_images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    },
)