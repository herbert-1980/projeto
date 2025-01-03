from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.forms import UserCreationForm
from django.utils.html import format_html 
from apps.accounts.models import MyUser
from apps.perfil.models import Perfil
from django.db import models


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'usuario'  # Certifique-se de que está associando corretamente ao campo 'usuario'
    
    
class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = MyUser
    inlines = [PerfilInline]
    list_display = ('email', 'username', 'get_profile_image','first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        ('Conta', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Históricos', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        
        # Verifica se o campo é um ImageField e se há uma imagem associada
        if isinstance(db_field, models.ImageField):
            if db_field.name == 'perfil.photo':  # Verifica o nome do campo de imagem
                # Acessa o perfil associado ao usuário atual
                if 'request' in kwargs:
                    usuario = kwargs['request'].user
                    try:
                        perfil = usuario.perfil
                        if perfil.photo:
                            # Exibe a miniatura ao lado do campo de upload
                            miniatura_html = format_html('<img src="{}" style="width: 50px; height: 50px; margin-left: 10px; border-radius: 50%;">', perfil.photo.url)
                            formfield.widget.attrs['help_text'] = miniatura_html
                    except Perfil.DoesNotExist:
                        pass
        
        return formfield

    def get_profile_image(self, obj):
        perfil = getattr(obj, 'perfil', None)  # Acessa o perfil relacionado
        if perfil and perfil.photo:  # Verifica se o perfil tem uma imagem
            return format_html('<img src="{}" style="height: 50px; width: 50px; border-radius: 50%;">', perfil.photo.url)
        return "Sem imagem"
    get_profile_image.short_description = "Imagem do Perfil"

    def get_phone(self, obj):
        return obj.perfil.phone if hasattr(obj, 'perfil') else "Sem telefone"
    get_phone.short_description = "Telefone"

    def get_birth_date(self, obj):
        return obj.perfil.birth_date if hasattr(obj, 'perfil') else "Sem data"
    get_birth_date.short_description = "Data de Nascimento"

admin.site.register(MyUser, MyUserAdmin)
