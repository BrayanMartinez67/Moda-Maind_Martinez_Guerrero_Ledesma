
from django.shortcuts import render, redirect, get_object_or_404
from Assessment.models import CategoriaSuperiorHombre, PrendaSuperiorHombre
from Assessment.forms import PrendaSuperiorHombreForm
from django.contrib.auth.decorators import login_required

@login_required
def vista_tren_superior_hombre(request):
    categorias = CategoriaSuperiorHombre.objects.all()
    prendas = PrendaSuperiorHombre.objects.filter(usuario=request.user)
    form = PrendaSuperiorHombreForm()

    if request.method == 'POST':
        form = PrendaSuperiorHombreForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('tren_superior_hombre')

    return render(request, 'core/Assessment/Armario_Digital/Boy/categorias_superior.html', {
        'categorias': categorias,
        'prendas': prendas,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),
    })


@login_required
def crear_prenda_superior_hombre(request):
    if request.method == 'POST':
        form = PrendaSuperiorHombreForm(request.POST, request.FILES)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.usuario = request.user
            prenda.save()
            return redirect('tren_superior_hombre')
    else:
        form = PrendaSuperiorHombreForm()
    return render(request, 'core/Assessment/Armario_Digital/Boy/categorias_superior.html', {'form': form})


@login_required
def editar_prenda_superior_hombre(request, pk):
    prenda = get_object_or_404(PrendaSuperiorHombre, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PrendaSuperiorHombreForm(request.POST, request.FILES, instance=prenda)
        if form.is_valid():
            form.save()
            return redirect('tren_superior_hombre')
    else:
        form = PrendaSuperiorHombreForm(instance=prenda)

    return render(request, 'core/Assessment/Armario_Digital/Boy/superior/editar_prenda.html', {'form': form, 'prenda': prenda})


@login_required
def eliminar_prenda_superior_hombre(request, pk):
    prenda = get_object_or_404(PrendaSuperiorHombre, pk=pk, usuario=request.user)
    prenda.delete()
    return redirect('tren_superior_hombre')
