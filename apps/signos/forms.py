from django import forms


class SignoForm(forms.Form):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data de Nascimento"
    )
