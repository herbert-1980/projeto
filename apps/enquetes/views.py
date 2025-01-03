from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from apps.enquetes.models import Enquete, Escolha, Voto
from apps.enquetes.forms import EnquetesForm
from django.template.loader import render_to_string


@login_required
def enquete(request):
    """Exibe a enquete ativa e processa a votação."""
    enquete = Enquete.objects.filter(ativo=True).first()
    if not enquete:
        return render(request, 'enquetes/enquete_form.html', {'error': 'Nenhuma enquete ativa no momento.'})

    # Verifica se o usuário já votou
    user_voted = Voto.objects.filter(user=request.user, enquete=enquete).exists()
    form = None if user_voted else EnquetesForm(enquete=enquete)

    if request.method == 'POST' and not user_voted:
        selected_escolha = get_object_or_404(Escolha, id=request.POST['escolha'])
        selected_escolha.votos += 1
        selected_escolha.save()

        # Registra o voto do usuário
        Voto.objects.create(user=request.user, enquete=enquete, escolha=selected_escolha)

        # Retorna os resultados para o AJAX
        results_html = render_to_string('enquetes/enquete_results.html', {'enquete': enquete})
        return JsonResponse({'results': results_html})
    
    elif user_voted:
        return JsonResponse({'error': 'Você já votou nesta enquete.'}, status=400)

    # Renderiza a página inicial com formulário ou sem, dependendo se o usuário votou
    return render(request, 'enquetes/enquete_form.html', {
        'enquete': enquete,
        'form': form,
        'user_voted': user_voted,
    })


@login_required
def enquete_detail(request, enquete_id):
    """Exibe os detalhes da enquete e permite votação."""
    enquete = get_object_or_404(Enquete, id=enquete_id)

    if request.method == 'POST':
        if Voto.objects.filter(user=request.user, enquete=enquete).exists():
            return render(request, 'enquetes/enquete_form.html', {
                'enquete': enquete,
                'show_results': True,
                'error': 'Você já votou nesta enquete.'
            })

        selected_escolha = get_object_or_404(Escolha, id=request.POST['escolha'])
        selected_escolha.votos += 1
        selected_escolha.save()

        Voto.objects.create(user=request.user, enquete=enquete, escolha=selected_escolha)

        return redirect('enquete:enquete_results', enquete_id=enquete.id)

    form = EnquetesForm(enquete=enquete)
    return render(request, 'enquetes/enquete_form.html', {'enquete': enquete, 'form': form})


@login_required
@require_GET
def enquete_results(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    escolhas = enquete.escolha.all()

    context = {
        'enquete': enquete,
        'escolhas': escolhas,
    }
    results_html = render_to_string('enquetes/enquete_results.html', context, request=request)

    return JsonResponse({'results': results_html})
    
@login_required
def enquete_vote(request, enquete_id):
    """Processa a votação para a enquete especificada."""
    enquete = get_object_or_404(Enquete, id=enquete_id)

    if request.method == 'POST':
        if Voto.objects.filter(user=request.user, enquete=enquete).exists():
            return JsonResponse({'error': 'Você já votou nesta enquete.'}, status=400)

        selected_escolha = get_object_or_404(Escolha, id=request.POST['escolha'])
        selected_escolha.votos += 1
        selected_escolha.save()

        Voto.objects.create(user=request.user, enquete=enquete, escolha=selected_escolha)

        # Renderiza os resultados para a resposta JSON
        results_html = render_to_string('enquete_results.html', {'enquete': enquete})
        return JsonResponse({'results': results_html})

    return JsonResponse({'error': 'Método não permitido.'}, status=405)
