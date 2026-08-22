from django.contrib import admin
from .models import Crianca

class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento', 'terapeuta')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(terapeuta=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.terapeuta:
            obj.terapeuta = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Crianca, CriancaAdmin)
