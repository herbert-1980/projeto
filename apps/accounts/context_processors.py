from django.conf import settings
from apps.accounts.models import MyUser  # Atualize o caminho conforme necessário


def user_count(request):
    return {
        'user_count': MyUser.objects.count(),
    }
