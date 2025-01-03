from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from io import BytesIO
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from apps.public_services.models import PublicUtility, LostAndFound
from apps.public_services.forms import LostAndFoundForm


# ----- UTILIDADES PÚBLICAS -----
def public_utilities(request):
    utilities = PublicUtility.objects.filter(is_active=True)
    return render(request, 'public_services/public_utilities.html', {'utilities': utilities})


# ----- ACHADOS E PERDIDOS -----
def lost_and_found(request):
    categoria = request.GET.get('categoria')
    if categoria:
        items = LostAndFound.objects.filter(is_active=True, categoria=categoria).order_by('-created_at')
    else:
        items = LostAndFound.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'public_services/lost_and_found.html', {'items': items})


def add_lost_and_found_item(request):
    if request.method == 'POST':
        form = LostAndFoundForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lost_and_found')  # Redireciona para a página de lista
    else:
        form = LostAndFoundForm()

    return render(request, 'public_services/add_lost_and_found.html', {'form': form})


def lost_and_found_list(request):
    items = LostAndFound.objects.all()
    search = request.GET.get('search', '')
    categoria = request.GET.get('categoria', '')
    location = request.GET.get('location', '')
    status = request.GET.get('status', '')
    date = request.GET.get('date', '')

    if search:
        items = items.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if categoria:
        items = items.filter(category=categoria)
    if location:
        items = items.filter(location__icontains=location)
    if status:
        items = items.filter(status=status)
    if date:
        items = items.filter(created_at__date=date)

    return render(request, 'lost_and_found.html', {'items': items})


def download_item(request, item_id):
    # Obter o item específico
    item = get_object_or_404(LostAndFound, id=item_id)
    
    # Validação: impedir download de itens inativos
    if not item.is_active:
        return HttpResponse("Este item não está ativo.", status=400)

    # Criar a resposta HTTP com o tipo de conteúdo "application/pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{slugify(item.title)}_detalhes.pdf"'

    # Criar o objeto PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Cabeçalho (logo + informações)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(150, 770, "CoophaNews - Notícias e Publicidades")
    c.setFont('Helvetica', 10)
    c.drawString(150, 755, "Endereço: Avenida Marinha, 1035, Coophavila 2 Campo Grande - MS")
    c.drawString(150, 740, "Telefone: (67) 99136-3900")
    c.drawString(150, 725, "Email: contato@coophanews.com.br")

    # Corpo do PDF (informações do item)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(30, 690, f"Item: {item.title}")
    c.setFont('Helvetica', 10)
    c.drawString(30, 675, f"Categoria: {item.get_categoria_display()}")
    c.drawString(30, 660, f"Status: {item.get_status_display()}")
    c.drawString(30, 645, f"Descrição: {item.description}")
    c.drawString(30, 630, f"Localização: {item.location}")
    
    # Rodapé (link atual)
    c.setFont('Helvetica-Oblique', 8)
    c.drawString(30, 15, f"Visitamos você em: {settings.SITE_URL}/utilidade-publica/achados-e-perdidos/")

    # Salvar o PDF no buffer
    c.showPage()
    c.save()

    # Devolver o buffer como um arquivo PDF
    buffer.seek(0)
    response.write(buffer.read())
    return response


@login_required
def pending_items(request):
    if not request.user.is_staff:
        raise PermissionDenied  # Bloqueia acesso se o usuário não for staff

    pending_items = LostAndFound.objects.filter(is_approved=False)
    return render(request, 'public_services/pending.html', {'pending_items': pending_items})
