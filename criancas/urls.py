from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_criancas, name='crianca_lista'),
    path('novo/', views.criar_crianca, name='crianca_criar'),
    path('<int:pk>/editar/', views.editar_crianca, name='crianca_editar'),
    path('<int:pk>/deletar/', views.deletar_crianca, name='crianca_deletar'),
]