from django import forms
from apps.enquetes.models import Escolha


class EnquetesForm(forms.Form):
    escolha = forms.ModelChoiceField(
        queryset=Escolha.objects.none(),  # Inicialmente vazio
        widget=forms.RadioSelect,
        empty_label=None,
        label="Escolha uma opção:"
    )

    def __init__(self, *args, **kwargs):
        enquete = kwargs.pop('enquete', None)  # Obtém a enquete do kwargs e remove-o
        super().__init__(*args, **kwargs)
        if enquete:
            self.fields['escolha'].queryset = enquete.escolha.all()
        else:
            # Se enquete não for passado, você pode definir um queryset vazio ou uma mensagem de erro
            self.fields['escolha'].queryset = Escolha.objects.none()
            # ou você pode levantar um erro personalizado
            raise ValueError("O objeto enquete deve ser fornecido ao formulário.")
        