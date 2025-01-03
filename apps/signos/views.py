from django.shortcuts import render
from apps.signos.models import Signo
from apps.signos.forms import SignoForm
from datetime import datetime


def obter_signo(dia, mes, ano):
    """
    Obtém o signo com base no dia, mês e ano.
    """
    for signo in Signo.objects.all():
        data_inicio = datetime.strptime(signo.data_inicio, "%d/%m").replace(year=ano)
        data_fim = datetime.strptime(signo.data_fim, "%d/%m").replace(year=ano)

        # Ajusta para signos que atravessam o final do ano
        if data_inicio > data_fim:
            
            if mes == 12:  # Para dezembro, ajustar o início ao ano atual
                data_fim = data_fim.replace(year=ano + 1)
            else:  # Para janeiro, ajustar o início ao ano anterior
                data_inicio = data_inicio.replace(year=ano - 1)

        # Verifica se a data de nascimento está no intervalo
        if data_inicio <= datetime(ano, mes, dia) <= data_fim:
            return signo
    return None


"""def signo_view(request):
    resultado = None
    if request.method == 'POST':
        form = SignoForm(request.POST)
        if form.is_valid():
            data_nascimento = form.cleaned_data['data_nascimento']  # Como datetime
            dia, mes, ano = data_nascimento.day, data_nascimento.month, data_nascimento.year  # Extraímos dia, mês, ano

            # Lógica para obter o signo com base no dia e mês
            resultado = obter_signo(dia, mes, ano)

    else:
        form = SignoForm()

    return render(request, 'signos/descobrir_signo.html', {'form': form, 'resultado': resultado})"""

def signo_view(request):
    resultado = None
    if request.method == 'POST':
        form = SignoForm(request.POST)
        if form.is_valid():
            # A data de nascimento que chega do formulário
            data_nascimento = form.cleaned_data['data_nascimento']
            
            # Pegando o dia, mês e ano da data de nascimento
            dia = data_nascimento.day
            mes = data_nascimento.month
            ano = data_nascimento.year

            # Passando os parâmetros para a função obter_signo
            resultado = obter_signo(dia, mes, ano)

    else:
        form = SignoForm()

    return render(request, 'signos/descobrir_signo.html', {'form': form, 'resultado': resultado})

