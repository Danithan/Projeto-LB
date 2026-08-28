from django.contrib import admin
from .models import SessaoModelo, SessaoRealizada, Tema
from criancas.models import Crianca


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor', 'icone', 'criado_em')
    search_fields = ('nome', 'descricao')


@admin.register(SessaoModelo)
class SessaoModeloAdmin(admin.ModelAdmin):
    list_display = ('numero', 'titulo', 'tema', 'faixa_etaria')
    list_filter = ('tema', 'faixa_etaria')
    search_fields = ('titulo', 'objetivo', 'descricao')
    ordering = ('numero',)

@admin.register(SessaoRealizada)
class SessaoRealizadaAdmin(admin.ModelAdmin):
    list_display = ('sessao_modelo', 'crianca', 'terapeuta', 'data', 'status')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(terapeuta=request.user)
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "crianca" and not request.user.is_superuser:
            kwargs["queryset"] = Crianca.objects.filter(terapeuta=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.terapeuta_id:
            obj.terapeuta = request.user
        super().save_model(request, obj, form, change)

