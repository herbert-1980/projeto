from django import forms
from apps.empresas.models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razao', 'fantasia', 'cnpj', 'logo', 'telefone',
            'rua', 'num', 'bairro', 'cep', 'cidade',
            'estado', 'categorias', 'latitude', 'longitude', 'mapa_url'
        ]
        widgets = {
            'razao': forms.TextInput(attrs={'class': 'form-control'}),
            'fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'num': forms.NumberInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Digite a latitude'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Digite a longitude'}),
            'mapa_url': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'razao': 'Razão Social',
            'fantasia': 'Nome Fantasia',
            'cnpj': 'CNPJ',
            'logo': 'Logo Marca',
            'telefone': 'Telefone',
            'rua': 'Rua',
            'num': 'Número',
            'bairro': 'Bairro',
            'cep': 'CEP',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'categorias': 'Categorias',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'mapa_url': 'URL do Mapa'
        }


    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise forms.ValidationError('A latitude deve estar entre -90 e 90.')
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise forms.ValidationError('A longitude deve estar entre -180 e 180.')
        return longitude
