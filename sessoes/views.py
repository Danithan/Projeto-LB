import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST
from weasyprint import HTML as WeasyHTML
from criancas.models import Crianca
from .models import SessaoRealizada, SessaoModelo
from exercicios.models import ExercicioModelo, ExercicioResultado


def _crianca_do_terapeuta_ou_404(request, crianca_id):
    if request.user.is_superuser:
        return get_object_or_404(Crianca, pk=crianca_id)
    return get_object_or_404(Crianca, pk=crianca_id, terapeuta=request.user)


def _formatar_duracao(total_segundos):
    total_segundos = total_segundos or 0
    minutos, segundos = divmod(total_segundos, 60)
    if minutos:
        return f"{minutos}min {segundos}s"
    return f"{segundos}s"


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


@login_required
def relatorio_sessao_pdf(request, sessao_id):
    if request.user.is_superuser:
        sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id)
    else:
        sessao_realizada = get_object_or_404(SessaoRealizada, pk=sessao_id, terapeuta=request.user)

    exercicios_modelo = ExercicioModelo.objects.filter(
        sessao_modelo=sessao_realizada.sessao_modelo
    ).order_by('numero')
    resultados_por_exercicio = {
        r.exercicio_modelo_id: r
        for r in ExercicioResultado.objects.filter(sessao_realizada=sessao_realizada)
    }
    linhas = [
        {'exercicio': ex, 'resultado': resultados_por_exercicio.get(ex.id)}
        for ex in exercicios_modelo
    ]
    respondidos = [linha['resultado'] for linha in linhas if linha['resultado']]
    media_percentual = (
        sum(r.percentual_acerto for r in respondidos) / len(respondidos)
        if respondidos else None
    )

    html_string = render_to_string('relatorios/sessao_pdf.html', {
        'sessao': sessao_realizada,
        'linhas': linhas,
        'total_exercicios': len(linhas),
        'total_respondidos': len(respondidos),
        'media_percentual': media_percentual,
        'gerado_em': timezone.now(),
    })
    pdf_bytes = WeasyHTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="sessao_{sessao_realizada.id}.pdf"'
    return response


@login_required
def relatorio_consolidado_pdf(request, crianca_id):
    crianca = _crianca_do_terapeuta_ou_404(request, crianca_id)

    linhas = []
    for sessao_realizada in SessaoRealizada.objects.filter(crianca=crianca).order_by('data'):
        resultados = ExercicioResultado.objects.filter(sessao_realizada=sessao_realizada)
        total_exercicios = ExercicioModelo.objects.filter(
            sessao_modelo=sessao_realizada.sessao_modelo
        ).count()
        media = resultados.aggregate(media=Avg('percentual_acerto'))['media']
        tempo_total = resultados.aggregate(total=Sum('tempo_segundos'))['total']
        linhas.append({
            'sessao': sessao_realizada,
            'total_exercicios': total_exercicios,
            'total_respondidos': resultados.count(),
            'media_percentual': media,
            'tempo_total': _formatar_duracao(tempo_total),
        })

    medias_validas = [linha['media_percentual'] for linha in linhas if linha['media_percentual'] is not None]
    media_geral = sum(medias_validas) / len(medias_validas) if medias_validas else None

    html_string = render_to_string('relatorios/consolidado_pdf.html', {
        'crianca': crianca,
        'linhas': linhas,
        'total_sessoes': len(linhas),
        'sessoes_concluidas': sum(1 for linha in linhas if linha['sessao'].status == 'concluida'),
        'media_geral': media_geral,
        'gerado_em': timezone.now(),
    })
    pdf_bytes = WeasyHTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="relatorio_{crianca.pk}.pdf"'
    return response
