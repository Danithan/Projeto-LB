from django.urls import path
from . import views

app_name = 'sessoes'

urlpatterns = [
    path('iniciar/<int:crianca_id>/', views.escolher_sessao, name='escolher_sessao'),
    path('relatorio/crianca/<int:crianca_id>/', views.relatorio_consolidado_pdf, name='relatorio_consolidado_pdf'),
    path('<int:sessao_id>/exercicios/<int:exercicio_id>/resultado/', views.salvar_resultado, name='salvar_resultado'),
    path('<int:sessao_id>/relatorio/', views.relatorio_sessao_pdf, name='relatorio_sessao_pdf'),
    path('<int:sessao_id>/', views.sessao_detail, name='sessao_detail'),
]
