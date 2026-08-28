from django.urls import path
from . import views

app_name = 'sessoes'

urlpatterns = [
    path('iniciar/<int:crianca_id>/', views.escolher_sessao, name='escolher_sessao'),
    path('montar/<int:crianca_id>/<int:sessao_modelo_id>/', views.montar_sessao, name='montar_sessao'),
    path('executar/<int:sessao_id>/', views.executar_sessao, name='executar_sessao'),
    path('finalizar/<int:sessao_id>/', views.finalizar_sessao, name='finalizar_sessao'),
    path('reiniciar/<int:sessao_id>/', views.reiniciar_sessao, name='reiniciar_sessao'),
    path('relatorio/html/<int:sessao_id>/', views.relatorio_sessao_html, name='relatorio_sessao_html'),
    path('relatorio/pdf/<int:sessao_id>/', views.relatorio_sessao_pdf, name='relatorio_sessao_pdf'),
    path('relatorio/crianca/<int:crianca_id>/', views.relatorio_consolidado_pdf, name='relatorio_consolidado_pdf'),
    path('<int:sessao_id>/exercicios/<int:exercicio_id>/resultado/', views.salvar_resultado, name='salvar_resultado'),
    path('<int:sessao_id>/', views.sessao_detail, name='sessao_detail'),
    path('exercicio/<int:exercicio_id>/editar/', views.editar_exercicio, name='editar_exercicio'),
    path('executar/<int:sessao_id>/inicio/<int:exercicio_id>/', views.exercicio_inicio, name='exercicio_inicio'),
    path('executar/<int:sessao_id>/jogar/<int:exercicio_id>/', views.jogar_exercicio, name='jogar_exercicio'),
]
