from django import forms
from datetime import datetime
from apps.news.models import News
from django_summernote.widgets import SummernoteWidget
from django.utils.text import slugify


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title', 'subtitle', 'slug_title', 'author', 'status', 'resume','content',
            'principal_image', 'video', 'source', 'views', 'share', 'categorias',
            'published_at', 'seo_title', 'seo_description', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da Notícia'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtítulo'}),
            'slug_title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Resumo da Notícia'}),
            'content': SummernoteWidget(attrs={'class': 'form-control'}),  # Campo com Summernote
            'principal_image': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL do Vídeo'}),
            'source': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Fonte da Notícia'}),
            'views': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'share': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'seo_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título SEO'}),
            'seo_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição SEO'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Campo de publicar
        }
        labels = {
            'title': 'Título',
            'principal_image': 'Imagem Principal',
            'author': 'Autor',
            'content': 'Conteúdo',
            'published_at': 'Data de Publicação',
            'resume': 'Resumo',
            'video': 'Vídeo',
            'source': 'Fonte',
            'categorias': 'Categorias',
            'is_published': 'Publicar Notícia',
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário e define campos como desabilitados."""
        super(NewsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['views'].widget.attrs['readonly'] = True
        self.fields['share'].widget.attrs['readonly'] = True

    def clean_published_at(self):
        """Valida o campo de data de publicação."""
        data = self.cleaned_data.get('published_at')
        if not isinstance(data, datetime):
            raise forms.ValidationError("Data inválida para 'published_at'")
        return data

    def save(self, commit=True):
        """Gera o slug automaticamente se estiver vazio e salva o objeto."""
        news = super().save(commit=False)
        if not news.slug_title:
            news.slug_title = slugify(news.title)
        if commit:
            news.save()
        return news
