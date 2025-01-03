from apps.banners.models import Banner


def banner_global(request):
    # Filtra os banners com destaque 4 (Capa)
    banners_vip = Banner.objects.filter(destaque=4)

    # Retorna todos os banners e o primeiro como banner global
    return {
        'banners_vip': banners_vip,  # Retorna todos os banners VIP
        'banner_global': banners_vip.first() if banners_vip.exists() else None,  # O primeiro banner VIP
    }
