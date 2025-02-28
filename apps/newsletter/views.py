from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import NewsletterForm
from .services import subscribe_to_newsletter


def subscribe_newsletter(request):
    if request.method == 'POST' and request.POST.get('form_type') =='newsletter_form':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscrição realizada com sucesso!")
            return redirect('home')
        else:
            messages.error(request, "Erro ao se inscrever na Newsletter.")  # Pode exibir a mensagem de erro no Toast

    return render(request, 'newsletter/subscribe.html', {'form': form})


class NewsletterSubscribeView(FormView):
    template_name = "newsletter/subscribe.html"
    form_class = NewsletterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Inscrição realizada com sucesso!")
        return super().form_valid(form)