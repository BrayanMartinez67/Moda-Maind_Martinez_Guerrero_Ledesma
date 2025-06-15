
from django.shortcuts import render, redirect, get_object_or_404
from Assessment.models import PrendaSuperiorMujer,CategoriaSuperiorMujer
from Assessment.forms import PrendaSuperiorMujerForm
from django.contrib.auth.decorators import login_required

@login_required
def vista_tren_superior_mujer(request):
    categorias = CategoriaSuperiorMujer.objects.all()
    prendas = PrendaSuperiorMujer.objects.filter(usuario=request.user)

    form = PrendaSuperiorMujerForm()

 
    if request.method == 'POST':
        form = PrendaSuperiorMujerForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('tren_superior_mujer')

    return render(request, 'core/Assessment/Armario_Digital/Girl/categorias.html', {
        'categorias': categorias,
        'prendas': prendas,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),  
    })


@login_required
def lista_prendas_superior(request):
    prendas = PrendaSuperiorMujer.objects.filter(usuario=request.user)
    categorias = CategoriaSuperiorMujer.objects.all()
    form = PrendaSuperiorMujerForm()

    if request.method == 'POST':
        form = PrendaSuperiorMujerForm(request.POST, request.FILES)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.save()
            return redirect('lista_prendas_mujer')

    return render(request, 'armario_mujer/lista_prendas.html', {
        'prendas': prendas,
        'categorias': categorias,
        'form': form,
        'form_con_errores': request.method == 'POST' and not form.is_valid(),  
    })

@login_required
def crear_prenda_superior(request):
    if request.method == 'POST':
        form = PrendaSuperiorMujerForm(request.POST, request.FILES)
        if form.is_valid():
            prenda = form.save(commit=False)
            prenda.usuario = request.user
            prenda.save()
            return redirect('tren_superior_mujer')
    else:
        form = PrendaSuperiorMujerForm()
    return render(request, 'core/Assessment/Armario_Digital/Girl/categorias.html', {'form': form})

@login_required
def eliminar_prenda_superior(request, pk):
    prenda = get_object_or_404(PrendaSuperiorMujer, pk=pk, usuario=request.user)
    prenda.delete()
    return redirect('tren_superior_mujer')


@login_required
def editar_prenda_superior(request, pk):
    prenda = get_object_or_404(PrendaSuperiorMujer, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = PrendaSuperiorMujerForm(request.POST, request.FILES, instance=prenda)
        if form.is_valid():
            form.save()
            return redirect('tren_superior_mujer')
    else:
        form = PrendaSuperiorMujerForm(instance=prenda)

    return render(request, 'core\Assessment\Armario_Digital\Girl\superior\editar_prenda.html', {'form': form ,'prenda': prenda})
