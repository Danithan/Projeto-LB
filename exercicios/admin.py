from django.contrib import admin
from .models import ExercicioModelo, ExercicioResultado

class ExercicioModeloAdmin(admin.ModelAdmin):
    pass # All admins can see models/templates

class ExercicioResultadoAdmin(admin.ModelAdmin):
    list_display = (
        'sessao_realizada',
        'exercicio_modelo',
        'percentual_acerto',
        'tentativas',
        'pontuacao',
        'tempo_segundos',
        'respondido_em',
    )
    list_filter = ('sessao_realizada__crianca', 'exercicio_modelo__tipo')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sessao_realizada__terapeuta=request.user)

admin.site.register(ExercicioModelo, ExercicioModeloAdmin)
admin.site.register(ExercicioResultado, ExercicioResultadoAdmin)
