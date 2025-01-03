from django.utils import timezone
from django.contrib.auth.models import User


def current_date(request):
    return {
        'current_date': timezone.now(),
    }

def user_count(request):
    count = User.objects.count()
    return {'user_count': count}