
from django.shortcuts import render, redirect, get_object_or_404
from Assessment.models import CategoriaCalzadoHombre, PrendaCalzadoHombre
from Assessment.forms import PrendaCalzadoHombreForm
from django.contrib.auth.decorators import login_required

@login_required
def vista_calzado_hombre(request):
    categorias = CategoriaCalzadoHombre.objects.all()
    prendas = PrendaCalzadoHombre.objects.filter(usuario=request.user)
    form = PrendaCalzadoHombreForm()

    if request.method == 'POST':
        form = PrendaCalzadoHombreForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('calzado_hombre')

    return render(request, 'core/Assessment/Armario_Digital/Boy/categorias_calzado.html', {
        'categorias': categorias,
        'prendas': prendas,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),
    })


@login_required
def crear_prenda_calzado_hombre(request):
    if request.method == 'POST':
        form = PrendaCalzadoHombreForm(request.POST, request.FILES)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.usuario = request.user
            prenda.save()
            return redirect('calzado_hombre')
    else:
        form = PrendaCalzadoHombreForm()
    return render(request, 'core/Assessment/Armario_Digital/Boy/categorias_calzado.html', {'form': form})


@login_required
def editar_prenda_calzado_hombre(request, pk):
    prenda = get_object_or_404(PrendaCalzadoHombre, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PrendaCalzadoHombreForm(request.POST, request.FILES, instance=prenda)
        if form.is_valid():
            form.save()
            return redirect('calzado_hombre')
    else:
        form = PrendaCalzadoHombreForm(instance=prenda)

    return render(request, 'core/Assessment/Armario_Digital/Boy/superior/editar_prenda.html', {'form': form, 'prenda': prenda})


@login_required
def eliminar_prenda_calzado_hombre(request, pk):
    prenda = get_object_or_404(PrendaCalzadoHombre, pk=pk, usuario=request.user)
    prenda.delete()
    return redirect('calzado_hombre')
