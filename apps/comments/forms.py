from django import forms
from apps.comments.models import Comment
import requests
from django.conf import settings

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ['comment_name', 'comment_email', 'comment']
        widgets = {
            'comment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
            'comment_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite seu comentário'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_name'].label = "Seu Nome"
        self.fields['comment_email'].label = "Seu Email"
        self.fields['comment'].label = "Seu Comentário"

    def clean(self):
        cleaned_data = super().clean()
        recaptcha_response = self.data.get('g-recaptcha-response')

        # Verifique se a chave secreta está nas configurações do Django
        recaptcha_secret_key = getattr(settings, 'RECAPTCHA_SECRET_KEY', None)
        if not recaptcha_secret_key:
            raise forms.ValidationError('Chave secreta do reCAPTCHA não configurada.')

        # Faz a requisição para o reCAPTCHA
        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': recaptcha_secret_key,
                'response': recaptcha_response
            }
        )

        recaptcha_result = recaptcha_request.json()
        if not recaptcha_result.get('success'):
            self.add_error(
                'comment',
                'Desculpe, ocorreu um erro com o reCAPTCHA. Tente novamente.'
            )

        return cleaned_data
