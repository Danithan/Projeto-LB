from django.contrib import admin
from .models import SessaoModelo, SessaoRealizada
from criancas.models import Crianca

class SessaoModeloAdmin(admin.ModelAdmin):
    pass # SessaoModelos are templates, so everyone sees them.

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

admin.site.register(SessaoModelo, SessaoModeloAdmin)
admin.site.register(SessaoRealizada, SessaoRealizadaAdmin)
