from django.urls import path
from . import views

app_name = 'sessoes'

urlpatterns = [
    path('iniciar/<int:crianca_id>/', views.escolher_sessao, name='escolher_sessao'),
    path('crianca/<int:crianca_id>/historico/', views.historico_crianca, name='historico_crianca'),
    path('relatorio/crianca/<int:crianca_id>/', views.relatorio_consolidado_pdf, name='relatorio_consolidado_pdf'),
    path('<int:sessao_id>/exercicios/<int:exercicio_id>/resultado/', views.salvar_resultado, name='salvar_resultado'),
    path('<int:sessao_id>/exercicios/<int:exercicio_id>/', views.exercicio_detail, name='exercicio_detail'),
    path('<int:sessao_id>/relatorio/', views.relatorio_sessao_pdf, name='relatorio_sessao_pdf'),
    path('<int:sessao_id>/finalizar/', views.finalizar_sessao, name='finalizar_sessao'),
    path('<int:sessao_id>/resultado/', views.resultado_sessao, name='resultado_sessao'),
    path('<int:sessao_id>/repetir/', views.repetir_sessao, name='repetir_sessao'),
    path('<int:sessao_id>/', views.sessao_detail, name='sessao_detail'),
]
