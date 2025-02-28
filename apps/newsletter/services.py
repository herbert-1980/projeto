from .models import NewsletterSubscriber


def subscribe_to_newsletter(email):
    if NewsletterSubscriber.objects.filter(email=email).exists():
        return False, "Este e-mail já está inscrito!"
    subscriber = NewsletterSubscriber.objects.create(email=email)
    return True, subscriber
