from django.shortcuts import render, get_object_or_404
from .models import SessaoRealizada
from exercicios.models import ExercicioModelo

def sessao_detail(request, sessao_id):
    sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id)
    # Get all exercises defined for this session's model
    exercicios_modelo = ExercicioModelo.objects.filter(sessao_modelo=sessao_realizada.sessao_modelo).order_by('numero')
    
    # We will pass the first exercise config as JSON, or all of them.
    # For now, let's pass a list of dicts with their id, numero, tipo, and configuracao
    exercicios_data = []
    for ex in exercicios_modelo:
        exercicios_data.append({
            'id': ex.id,
            'numero': ex.numero,
            'tipo': ex.tipo,
            'enunciado': ex.enunciado,
            'configuracao': ex.configuracao,
        })
        
    return render(request, 'sessoes/sessao_detail.html', {
        'sessao': sessao_realizada,
        'exercicios_data': exercicios_data,
    })
