import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
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


def _sessao_do_terapeuta_ou_404(request, sessao_id):
    if request.user.is_superuser:
        return get_object_or_404(SessaoRealizada, pk=sessao_id)
    return get_object_or_404(SessaoRealizada, pk=sessao_id, terapeuta=request.user)


def _formatar_duracao(total_segundos):
    total_segundos = total_segundos or 0
    minutos, segundos = divmod(total_segundos, 60)
    if minutos:
        return f"{minutos}min {segundos}s"
    return f"{segundos}s"


def _linhas_resultado(sessao_realizada):
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
    tempo_total = sum((r.tempo_segundos or 0) for r in respondidos)
    return linhas, respondidos, media_percentual, tempo_total


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

    ultimas_por_modelo = {}
    for sr in SessaoRealizada.objects.filter(crianca=crianca).order_by('sessao_modelo_id', '-data'):
        ultimas_por_modelo.setdefault(sr.sessao_modelo_id, sr)

    sessoes_status = []
    for sessao_modelo in SessaoModelo.objects.order_by('numero'):
        ultima = ultimas_por_modelo.get(sessao_modelo.id)
        if ultima is None:
            status, sessao_realizada_id = 'pendente', None
        elif ultima.status == 'concluida':
            status, sessao_realizada_id = 'concluida', ultima.id
        else:
            status, sessao_realizada_id = 'em_andamento', ultima.id
        sessoes_status.append({
            'modelo': sessao_modelo,
            'status': status,
            'sessao_realizada_id': sessao_realizada_id,
        })

    concluidas = sum(1 for s in sessoes_status if s['status'] == 'concluida')
    total = len(sessoes_status) or 1

    return render(request, 'sessoes/escolher_sessao.html', {
        'crianca': crianca,
        'sessoes_status': sessoes_status,
        'progresso_percentual': round(concluidas * 100 / total),
        'active': 'sessoes',
    })


ICONE_POR_TIPO = {
    'pergunta_aberta': 'quiz',
    'jogo_palavras': 'extension',
    'multipla_escolha': 'checklist',
    'verdadeiro_falso': 'fact_check',
    'caca_palavras': 'grid_view',
    'cruzadinha': 'grid_on',
    'ordena_letras': 'sort_by_alpha',
    'preenche_lacunas_letras': 'edit_note',
}


@login_required
def sessao_detail(request, sessao_id):
    """Tela 1e — grade de exercícios da sessão em andamento."""
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)

    exercicios_modelo = list(
        ExercicioModelo.objects.filter(sessao_modelo=sessao_realizada.sessao_modelo).order_by('numero')
    )
    feitos_ids = set(
        ExercicioResultado.objects.filter(sessao_realizada=sessao_realizada)
        .values_list('exercicio_modelo_id', flat=True)
    )
    for ex in exercicios_modelo:
        ex.feito = ex.id in feitos_ids
        ex.icone = ICONE_POR_TIPO.get(ex.tipo, 'extension')

    return render(request, 'sessoes/sessao_detail.html', {
        'sessao': sessao_realizada,
        'crianca': sessao_realizada.crianca,
        'exercicios_modelo': exercicios_modelo,
        'total_feitos': len(feitos_ids),
        'total_exercicios': len(exercicios_modelo),
        'active': 'sessoes',
    })


@login_required
def exercicio_detail(request, sessao_id, exercicio_id):
    """Telas 1f/1g — um exercício por vez."""
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)
    exercicio = get_object_or_404(
        ExercicioModelo, pk=exercicio_id, sessao_modelo=sessao_realizada.sessao_modelo
    )

    exercicios_data = [{
        'id': exercicio.id,
        'numero': exercicio.numero,
        'tipo': exercicio.tipo,
        'enunciado': exercicio.enunciado,
        'configuracao': exercicio.configuracao,
        'icone': ICONE_POR_TIPO.get(exercicio.tipo, 'quiz'),
    }]

    return render(request, 'sessoes/exercicio_detail.html', {
        'sessao': sessao_realizada,
        'crianca': sessao_realizada.crianca,
        'exercicio': exercicio,
        'exercicios_data': exercicios_data,
        'active': 'sessoes',
    })


@login_required
@require_POST
def salvar_resultado(request, sessao_id, exercicio_id):
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)

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
        'proxima_url': reverse('sessoes:sessao_detail', args=[sessao_realizada.id]),
    })


@login_required
@require_POST
def finalizar_sessao(request, sessao_id):
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)
    sessao_realizada.status = 'concluida'
    sessao_realizada.save(update_fields=['status'])
    return redirect('sessoes:resultado_sessao', sessao_id=sessao_realizada.id)


@login_required
def resultado_sessao(request, sessao_id):
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)
    linhas, respondidos, media_percentual, tempo_total = _linhas_resultado(sessao_realizada)

    return render(request, 'sessoes/resultado_sessao.html', {
        'sessao': sessao_realizada,
        'crianca': sessao_realizada.crianca,
        'linhas': linhas,
        'total_exercicios': len(linhas),
        'total_respondidos': len(respondidos),
        'media_percentual': media_percentual,
        'tempo_total_formatado': _formatar_duracao(tempo_total),
        'active': 'sessoes',
    })


@login_required
def repetir_sessao(request, sessao_id):
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)

    if request.method == 'POST':
        ExercicioResultado.objects.filter(sessao_realizada=sessao_realizada).delete()
        sessao_realizada.status = 'em_andamento'
        sessao_realizada.data = timezone.now()
        sessao_realizada.save(update_fields=['status', 'data'])
        return redirect('sessoes:sessao_detail', sessao_id=sessao_realizada.id)

    return render(request, 'sessoes/confirmar_repeticao.html', {
        'sessao': sessao_realizada,
        'crianca': sessao_realizada.crianca,
        'active': 'sessoes',
    })


@login_required
def historico_crianca(request, crianca_id):
    crianca = _crianca_do_terapeuta_ou_404(request, crianca_id)

    todas_qs = SessaoRealizada.objects.filter(crianca=crianca).order_by('-data')
    mostrar_todas = request.GET.get('todas') == '1'
    sessoes_qs = todas_qs if mostrar_todas else todas_qs[:5]

    sessoes_info = []
    for sr in sessoes_qs:
        resultados = ExercicioResultado.objects.filter(sessao_realizada=sr)
        media = resultados.aggregate(media=Avg('percentual_acerto'))['media']
        tempo_total = resultados.aggregate(total=Sum('tempo_segundos'))['total']
        sessoes_info.append({
            'sessao': sr,
            'media_percentual': media,
            'tempo_total_formatado': _formatar_duracao(tempo_total),
            'total_respondidos': resultados.count(),
        })

    return render(request, 'sessoes/historico_crianca.html', {
        'crianca': crianca,
        'sessoes_info': sessoes_info,
        'tem_mais': (not mostrar_todas) and todas_qs.count() > 5,
        'active': 'historico',
    })


@login_required
def relatorio_sessao_pdf(request, sessao_id):
    sessao_realizada = _sessao_do_terapeuta_ou_404(request, sessao_id)
    linhas, respondidos, media_percentual, _tempo_total = _linhas_resultado(sessao_realizada)

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
