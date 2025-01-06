from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


def current_date(request):
    return {
        'current_date': timezone.now(),
    }

def user_count(request):
    count = User.objects.count()
    return {'user_count': count}

def local_date(request):
    # Obtém a data atual
    local_date = timezone.now()
    # Formata a data no formato desejado
    formatted_date = local_date.strftime("%A, %d de %B de %Y")
    translated_date = _(formatted_date)
    return {
        'local_date': translated_date,
    }