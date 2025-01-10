from django.shortcuts import render
from django.core.mail import send_mail
from apps.contatos.forms import ContatoForm


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            # Salva no banco de dados
            form.save()

            # Envia o email
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            mensagem = form.cleaned_data['mensagem']
            send_mail(
                f'Contato de {nome}',
                mensagem,
                email,
                ['contato@coophanews.com.br'],  # Altere para o seu email
                fail_silently=False,
            )
            return render(request, 'contatos/sucesso.html')
    else:
        form = ContatoForm()

    return render(request, 'contatos/contatos.html', {'form': form})
