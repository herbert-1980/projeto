from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from apps.promocoes.forms import PromocaoForm
from apps.promocoes.models import Promocao, ImagemPromocao


def lista_promocoes(request):
    promocoes = Promocao.objects.filter(data_fim__gte=datetime.now())
    # Processando o nome da empresa para remover o CNPJ
    for promocao in promocoes:
        nome_empresa = promocao.empresa.fantasia.split(' - ')[0]  # Divide e pega apenas o nome da empresa
        promocao.empresa_nome = nome_empresa  # Adiciona o nome processado ao contexto

    return render(request, "promocoes/lista_promocoes.html", {"promocoes": promocoes})

def detalhes_promocao(request, promocao_id):
    promocao = get_object_or_404(Promocao, id=promocao_id)
    return render(request, "promocoes/detalhes_promocao.html", {"promocao": promocao})

def criar_promocao(request):
    if request.method == 'POST':
        promocao_form = PromocaoForm(request.POST, request.FILES)
        imagens = request.FILES.getlist('imagens')  # Obtém todas as imagens enviadas

        if promocao_form.is_valid():
            promocao = promocao_form.save()  # Salva a promoção
            
            # Itera sobre as imagens enviadas e cria instâncias de ImagemPromocao
            for imagem in imagens:
                ImagemPromocao.objects.create(promocao=promocao, imagem=imagem)
            
            return redirect('lista_promocoes')  # Redireciona após salvar
            
    else:
        promocao_form = PromocaoForm()
    
    return render(request, 'promocoes/criar_promocao.html', {
        'promocao_form': promocao_form,
    })
