from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from criancas.models import Crianca
from .forms import CriancaForm


def _crianca_do_terapeuta_ou_404(request, pk):
    if request.user.is_superuser:
        return get_object_or_404(Crianca, pk=pk)
    return get_object_or_404(Crianca, pk=pk, terapeuta=request.user)


@login_required
def lista_criancas(request):
    if request.user.is_superuser:
        criancas_list = Crianca.objects.all()
    else:
        criancas_list = Crianca.objects.filter(terapeuta=request.user)
    return render(request, 'criancas/crianca_lista.html', {'criancas': criancas_list})


@login_required
def criar_crianca(request):
    if request.method == 'POST':
        form = CriancaForm(request.POST)
        if form.is_valid():
            crianca = form.save(commit=False)
            crianca.terapeuta = request.user
            crianca.save()
            return redirect('crianca_lista')
    else:
        form = CriancaForm()
    return render(request, 'criancas/crianca_form.html', {'form': form})


@login_required
def editar_crianca(request, pk):
    crianca = _crianca_do_terapeuta_ou_404(request, pk)
    if request.method == 'POST':
        form = CriancaForm(request.POST, instance=crianca)
        if form.is_valid():
            form.save()
            return redirect('crianca_lista')
    else:
        form = CriancaForm(instance=crianca)
    return render(request, 'criancas/crianca_form.html', {'form': form})


@login_required
def deletar_crianca(request, pk):
    crianca = _crianca_do_terapeuta_ou_404(request, pk)
    if request.method == 'POST':
        crianca.delete()
        return redirect('crianca_lista')
    return render(request, 'criancas/crianca_confirmar_delete.html', {'crianca': crianca})
