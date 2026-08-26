import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from criancas.models import Crianca
from .models import SessaoRealizada, SessaoModelo
from exercicios.models import ExercicioModelo, ExercicioResultado


def _crianca_do_terapeuta_ou_404(request, crianca_id):
    if request.user.is_superuser:
        return get_object_or_404(Crianca, pk=crianca_id)
    return get_object_or_404(Crianca, pk=crianca_id, terapeuta=request.user)


@login_required
def escolher_sessao(request, crianca_id):
    crianca = _crianca_do_terapeuta_ou_404(request, crianca_id)

    if request.method == 'POST':
        sessao_modelo = get_object_or_404(SessaoModelo, pk=request.POST.get('sessao_modelo_id'))
        sessao_realizada = SessaoRealizada.objects.create(
            crianca=crianca,
            sessao_modelo=sessao_modelo,
            terapeuta=request.user,
            data=timezone.now(),
            status='em_andamento',
        )
        return redirect('sessoes:sessao_detail', sessao_id=sessao_realizada.id)

    sessoes_modelo = SessaoModelo.objects.order_by('numero')
    return render(request, 'sessoes/escolher_sessao.html', {
        'crianca': crianca,
        'sessoes_modelo': sessoes_modelo,
    })


@login_required
def sessao_detail(request, sessao_id):
    if request.user.is_superuser:
        sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id)
    else:
        sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id, terapeuta=request.user)

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


@login_required
@require_POST
def salvar_resultado(request, sessao_id, exercicio_id):
    if request.user.is_superuser:
        sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id)
    else:
        sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id, terapeuta=request.user)

    exercicio = get_object_or_404(
        ExercicioModelo, pk=exercicio_id, sessao_modelo=sessao_realizada.sessao_modelo
    )

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    try:
        percentual_acerto = Decimal(str(payload.get('percentual_acerto', 0)))
    except InvalidOperation:
        return JsonResponse({'erro': 'percentual_acerto inválido'}, status=400)

    tempo_segundos = int(payload.get('tempo_segundos', 0) or 0)
    pontuacao = int(payload.get('pontuacao', 0) or 0)

    resultado = ExercicioResultado.objects.filter(
        sessao_realizada=sessao_realizada, exercicio_modelo=exercicio
    ).first()

    if resultado is None:
        proxima_ordem = ExercicioResultado.objects.filter(sessao_realizada=sessao_realizada).count() + 1
        resultado = ExercicioResultado.objects.create(
            sessao_realizada=sessao_realizada,
            exercicio_modelo=exercicio,
            ordem_execucao=proxima_ordem,
            percentual_acerto=percentual_acerto,
            tentativas=1,
            tempo_segundos=tempo_segundos,
            pontuacao=pontuacao,
        )
    else:
        resultado.tentativas += 1
        resultado.percentual_acerto = percentual_acerto
        resultado.tempo_segundos = tempo_segundos
        resultado.pontuacao = pontuacao
        resultado.save()

    return JsonResponse({
        'ok': True,
        'tentativas': resultado.tentativas,
        'percentual_acerto': str(resultado.percentual_acerto),
    })
