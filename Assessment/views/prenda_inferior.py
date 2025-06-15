
from django.shortcuts import render, redirect, get_object_or_404
from Assessment.models import CategoriaInferiorMujer, PrendaInferiorMujer
from Assessment.forms import PrendaInferiorMujerForm, PrendaInferiorMujer
from django.contrib.auth.decorators import login_required

@login_required
def vista_tren_inferior_mujer(request):
    categorias = CategoriaInferiorMujer.objects.all()
    prendas = PrendaInferiorMujer.objects.filter(usuario=request.user)
    form = PrendaInferiorMujerForm()

    if request.method == 'POST':
        form = PrendaInferiorMujerForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('tren_inferior_mujer')

    return render(request, 'core/Assessment/Armario_Digital/Girl/categorias_inferior.html', {
        'categorias': categorias,
        'prendas': prendas,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),
    })


@login_required
def crear_prenda_inferior(request):
    form = PrendaInferiorMujerForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        prenda = form.save(commit=False)
        prenda.usuario = request.user
        prenda.save()
        return redirect('tren_inferior_mujer')
    return render(request, 'core/Assessment/Armario_Digital/Girl/categorias_inferior.html', {'form': form})


@login_required
def editar_prenda_inferior(request, pk):
    prenda = get_object_or_404(PrendaInferiorMujer, pk=pk, usuario=request.user)
    form = PrendaInferiorMujerForm(request.POST or None, request.FILES or None, instance=prenda)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('tren_inferior_mujer')
    return render(request, 'core/Assessment/Armario_Digital/Girl/superior/editar_prenda.html', {'form': form, 'prenda': prenda})


@login_required
def eliminar_prenda_inferior(request, pk):
    prenda = get_object_or_404(PrendaInferiorMujer, pk=pk, usuario=request.user)
    prenda.delete()
    return redirect('tren_inferior_mujer')
