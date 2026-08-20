from django.shortcuts import get_object_or_404, render, redirect
from criancas.models import Crianca
from .forms import CriancaForm

def lista_criancas(request):
    criancas_list = Crianca.objects.all()
    return render(request, 'criancas/crianca_lista.html', {'criancas': criancas_list})

def criar_crianca(request):
    if request.method == 'POST':
        form = CriancaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crianca_lista')
    else:
        form = CriancaForm()
    return render(request, 'criancas/crianca_form.html', {'form': form})

def editar_crianca(request, pk):
    crianca = get_object_or_404(Crianca, pk=pk)
    if request.method == 'POST':
        form = CriancaForm(request.POST, instance=crianca)
        if form.is_valid():
            form.save()
            return redirect('crianca_lista')
    else:
        form = CriancaForm(instance=crianca)
    return render(request, 'criancas/crianca_form.html', {'form': form})

def deletar_crianca(request, pk):
    crianca = get_object_or_404(Crianca, pk=pk)
    if request.method == 'POST':
        crianca.delete()
        return redirect('crianca_lista')
    return render(request, 'criancas/crianca_confirmar_delete.html', {'crianca': crianca})