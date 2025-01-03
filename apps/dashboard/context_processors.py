from datetime import datetime


def greeting_processor(request):
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Bom dia!"
    elif 12 <= current_hour < 18:
        greeting = "Boa tarde!"
    else:
        greeting = "Boa noite!"

    return {'greeting': greeting}

def calcular_idade(data_nascimento):
    hoje = datetime.now()
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    return idade

def idade_context(request):
    idade = None  # Define a variável idade inicialmente como None
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)  # Usando getattr para evitar erro se o perfil não existir
        if perfil and perfil.birth_date:  # Verifica se perfil existe e tem data de nascimento
            idade = calcular_idade(perfil.birth_date)
    return {
        'idade': idade
    }

