from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import OutfitForm
import os
from django.conf import settings
from django.core.files.storage import default_storage
from ..forms import EvaluacionForm
from ..models import TipoCuerpo, Evento, Lugar
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Outfit


def subir_foto(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        imagen = request.FILES['imagen']
        outfit = Outfit.objects.create(imagen=imagen)
        return JsonResponse({'mensaje': 'Imagen guardada', 'outfit_id': outfit.id})
    return JsonResponse({'error': 'Método no permitido o sin imagen'}, status=400)

def evaluacion(request, outfit_id):
    outfit = get_object_or_404(Outfit, id=outfit_id)
    genero = request.GET.get('genero')
    return render(request, 'core/Assessment/moda/evaluacion.html', {
        'outfit': outfit,
        'genero': genero
    })


def subir_outfit(request):
    if request.method == 'POST':
        if request.content_type.startswith('multipart/form-data'):
            form = OutfitForm(request.POST, request.FILES)
            if form.is_valid():
                outfit = form.save(commit=False)

            
                carpeta = ''
                ruta_carpeta = os.path.join(settings.MEDIA_ROOT, carpeta)
                if not os.path.exists(ruta_carpeta):
                    os.makedirs(ruta_carpeta)

                archivos = os.listdir(ruta_carpeta)
                fotos_existentes = [f for f in archivos if f.startswith('foto') and f.endswith(('.jpg', '.jpeg', '.png'))]

                numeros = []
                for f in fotos_existentes:
                    nombre_sin_ext = os.path.splitext(f)[0]
                    num_str = nombre_sin_ext.replace('foto', '')
                    if num_str.isdigit():
                        numeros.append(int(num_str))

                siguiente_numero = max(numeros) + 1 if numeros else 1
                extension = os.path.splitext(outfit.imagen.name)[1]
                nuevo_nombre = f"foto{siguiente_numero}{extension}"
                outfit.imagen.name = carpeta + nuevo_nombre

                outfit.save()

            
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    imagen_url = outfit.imagen.url
                    return JsonResponse({'mensaje': 'Foto subida con éxito', 'imagen_url': imagen_url})

                return redirect('subir_outfit')
            else:
                return JsonResponse({'error': 'Formulario inválido'}, status=400)
        else:
            return JsonResponse({'error': 'Tipo de contenido no soportado'}, status=400)
    else:
        form = OutfitForm()
    
    return render(request, 'core/Assessment/moda/subir.html', {'form': form})


def subir_evaluacion(request):
    eventos = Evento.objects.all()
    lugares = Lugar.objects.all()
    tipos_cuerpo = TipoCuerpo.objects.all()
    return render(request, 'Assessment/subir.html', {
        'eventos_json': json.dumps(list(eventos.values('id', 'nombre')), cls=DjangoJSONEncoder),
        'lugares_json': json.dumps(list(lugares.values('id', 'nombre')), cls=DjangoJSONEncoder),
        'tipos_cuerpo_json': json.dumps(list(tipos_cuerpo.values('id', 'nombre')), cls=DjangoJSONEncoder),
    })


def guardar_evaluacion(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


def handle_uploaded_image(imagen):

    folder_path = os.path.join(settings.MEDIA_ROOT, 'outfits')

 
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    fs = FileSystemStorage(location=folder_path)
    filename = fs.save(imagen.name, imagen)
    imagen_url = fs.url(filename)  

    return imagen_url

@csrf_exempt
def subir_imagen(request):
    
    if request.method == 'POST' and request.FILES.get('imagen'):
        imagen = request.FILES['imagen']
        imagen_url = handle_uploaded_image(imagen)  
        return JsonResponse({
            'mensaje': 'Imagen guardada con éxito',
            'imagen_url': imagen_url  
        })
    return JsonResponse({'mensaje': 'No se pudo procesar la imagen'}, status=400)
def evaluacion_formulario(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok'}) 
        else:
            return JsonResponse({'status': 'error', 'errores': form.errors}, status=400)

    eventos = Evento.objects.all()
    lugares = Lugar.objects.all()
    tipos_cuerpo = TipoCuerpo.objects.all()
    imagen_url = request.GET.get('imagen_url', '')

    return render(request, 'core/Assessment/moda/evaluacion.html', {
        'eventos': eventos,
        'lugares': lugares,
        'tipos_cuerpo': tipos_cuerpo,
        'imagen_url': imagen_url,
        'ok': True
    })

def evaluacion_view(request):
    genero = request.GET.get('genero', 'hombre')
    imagen_url = request.GET.get('imagen_url', '')
    return render(request, 'evaluacion.html', {
        'genero': genero,
        'imagen_url': imagen_url,
    })

from django.shortcuts import render




def armario_hombre(request):
    return render(request, 'core\Assessment\man.html')

def armario_mujer(request):
    return render(request, 'core\Assessment\girl.html')

from django.shortcuts import render, redirect
from Assessment.models import CategoriaSuperiorMujer, PrendaSuperiorMujer
from django.contrib.auth.decorators import login_required

@login_required
def armario_mujer_tren_superior(request):
    categorias = CategoriaSuperiorMujer.objects.all()
    return render(request, 'armario_mujer/tren_superior.html', {
        'categorias': categorias
    })
