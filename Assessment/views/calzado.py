
from django.shortcuts import render, redirect, get_object_or_404
from Assessment.models import CategoriaCalzadoMujer, PrendaCalzadoMujer
from Assessment.forms import PrendaCalzadoMujerForm
from django.contrib.auth.decorators import login_required

@login_required
def vista_calzado_mujer(request):
    categorias = CategoriaCalzadoMujer.objects.all()
    prendas = PrendaCalzadoMujer.objects.filter(usuario=request.user)
    form = PrendaCalzadoMujerForm()

    if request.method == 'POST':
        form = PrendaCalzadoMujerForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('calzado_mujer')

    return render(request, 'core/Assessment/Armario_Digital/Girl/categorias_calzado.html', {
        'categorias': categorias,
        'prendas': prendas,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),
    })


@login_required
def crear_prenda_calzado(request):
    if request.method == 'POST':
        form = PrendaCalzadoMujerForm(request.POST, request.FILES)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.usuario = request.user
            prenda.save()
            return redirect('calzado_mujer')
    else:
        form = PrendaCalzadoMujerForm()
    return render(request, 'core/Assessment/Armario_Digital/Girl/categorias_calzado.html', {'form': form})


@login_required
def editar_prenda_calzado(request, pk):
    prenda = get_object_or_404(PrendaCalzadoMujer, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PrendaCalzadoMujerForm(request.POST, request.FILES, instance=prenda)
        if form.is_valid():
            form.save()
            return redirect('calzado_mujer')
    else:
        form = PrendaCalzadoMujerForm(instance=prenda)

    return render(request, 'core/Assessment/Armario_Digital/Girl/superior/editar_prenda.html', {'form': form, 'prenda': prenda})


@login_required
def eliminar_prenda_calzado(request, pk):
    prenda = get_object_or_404(PrendaCalzadoMujer, pk=pk, usuario=request.user)
    prenda.delete()
    return redirect('calzado_mujer')
