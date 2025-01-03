from django import forms
from apps.perfil.models import Perfil, Empresa


class PerfilForm(forms.ModelForm):
    is_cnpj = forms.BooleanField(required=False, label='Cadastrar como CNPJ')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),  # gera pro campo 3 linhas somente
        max_length=200
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(
        attrs={'id': 'id_birth_date', 'class': 'form-control', 'placeholder': 'Selecione a data de nascimento',
               'type': 'date'})
    )

    class Meta:
        model = Perfil
        fields = ['photo', 'occupation', 'description', 'gender', 'phone', 'birth_date', 'group_blood','rh_factor', 'weight', 'street', 'house_number', 'neighborhood',
                  'city', 'state', 'cpf', 'rg', 'academic_qualification',  'is_cnpj', 'empresa',]
        widgets = {
            'gender': forms.Select,
            'state': forms.Select,
        }

    # Para colocar as classes do Bootstrap
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerfilForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
