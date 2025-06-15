
from django.shortcuts import render, redirect, get_object_or_404
from Assessment.models import CategoriaInferiorHombre, PrendaInferiorHombre
from Assessment.forms import PrendaInferiorHombreForm
from django.contrib.auth.decorators import login_required

@login_required
def vista_tren_inferior_hombre(request):
    categorias = CategoriaInferiorHombre.objects.all()
    prendas = PrendaInferiorHombre.objects.filter(usuario=request.user)
    form = PrendaInferiorHombreForm()

    if request.method == 'POST':
        form = PrendaInferiorHombreForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('tren_inferior_hombre')

    return render(request, 'core/Assessment/Armario_Digital/Boy/categorias_inferior.html', {
        'categorias': categorias,
        'prendas': prendas,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),
    })


@login_required
def crear_prenda_inferior_hombre(request):
    if request.method == 'POST':
        form = PrendaInferiorHombreForm(request.POST, request.FILES)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.usuario = request.user
            prenda.save()
            return redirect('tren_inferior_hombre')
    else:
        form = PrendaInferiorHombreForm()
    return render(request, 'core/Assessment/Armario_Digital/Boy/categorias_inferior.html', {'form': form})


@login_required
def editar_prenda_inferior_hombre(request, pk):
    prenda = get_object_or_404(PrendaInferiorHombre, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PrendaInferiorHombreForm(request.POST, request.FILES, instance=prenda)
        if form.is_valid():
            form.save()
            return redirect('tren_inferior_hombre')
    else:
        form = PrendaInferiorHombreForm(instance=prenda)

    return render(request, 'core/Assessment/Armario_Digital/Boy/superior/editar_prenda.html', {'form': form, 'prenda': prenda})


@login_required
def eliminar_prenda_inferior_hombre(request, pk):
    prenda = get_object_or_404(PrendaInferiorHombre, pk=pk, usuario=request.user)
    prenda.delete()
    return redirect('tren_inferior_hombre')
