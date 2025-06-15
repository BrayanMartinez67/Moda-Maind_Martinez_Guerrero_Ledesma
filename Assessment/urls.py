from django.urls import path
from .views.views import subir_foto, evaluacion, evaluacion_formulario, armario_hombre, armario_mujer, armario_mujer_tren_superior
from .views.prenda_superior import lista_prendas_superior, crear_prenda_superior, eliminar_prenda_superior,editar_prenda_superior, vista_tren_superior_mujer
from.views.prenda_inferior import vista_tren_inferior_mujer, crear_prenda_inferior, editar_prenda_inferior, eliminar_prenda_inferior
from .views.calzado import vista_calzado_mujer, crear_prenda_calzado, editar_prenda_calzado, eliminar_prenda_calzado
from .views.prenda_superior_hombre import vista_tren_superior_hombre, crear_prenda_superior_hombre, editar_prenda_superior_hombre, eliminar_prenda_superior_hombre
from .views.prenda_inferior_hombre import vista_tren_inferior_hombre, crear_prenda_inferior_hombre, editar_prenda_inferior_hombre, eliminar_prenda_inferior_hombre
from .views.calzado_hombre import vista_calzado_hombre, crear_prenda_calzado_hombre, editar_prenda_calzado_hombre, eliminar_prenda_calzado_hombre
urlpatterns = [
    path('subir-foto/', subir_foto, name='subir_foto'),
    path('evaluacion/<int:outfit_id>/', evaluacion, name='evaluacion'),
    path('evaluacion/', evaluacion_formulario, name='evaluacion_formulario'),
    path('armario/hombre/', armario_hombre, name='armario_hombre'),
    path('armario/mujer/', armario_mujer, name='armario_mujer'),
    path('armario/mujer/superior/', armario_mujer_tren_superior, name='armario_mujer_superior'),
    path('armario/mujer/tren-superior/', vista_tren_superior_mujer, name='tren_superior_mujer'),
    path('mujer/', lista_prendas_superior, name='lista_prendas_mujer'),
    path('mujer/editar/<int:pk>/', editar_prenda_superior, name='editar_prenda_mujer'),
    path('mujer/nueva/', crear_prenda_superior, name='crear_prenda_mujer'),
    path('mujer/eliminar/<int:pk>/', eliminar_prenda_superior, name='eliminar_prenda_mujer'), 
    path('armario/mujer/tren-inferior/', vista_tren_inferior_mujer, name='tren_inferior_mujer'),
    path('mujer/inferior/nueva/', crear_prenda_inferior, name='crear_prenda_inferior'),
    path('mujer/inferior/editar/<int:pk>/', editar_prenda_inferior, name='editar_prenda_inferior'),
    path('mujer/inferior/eliminar/<int:pk>/', eliminar_prenda_inferior, name='eliminar_prenda_inferior'),
    path('armario/mujer/calzado/', vista_calzado_mujer, name='calzado_mujer'),
    path('mujer/calzado/nueva/', crear_prenda_calzado, name='crear_prenda_calzado'),
    path('mujer/calzado/editar/<int:pk>/', editar_prenda_calzado, name='editar_prenda_calzado'),
    path('mujer/calzado/eliminar/<int:pk>/', eliminar_prenda_calzado, name='eliminar_prenda_calzado'),
    path('armario/hombre/tren-superior/', vista_tren_superior_hombre, name='tren_superior_hombre'),
    path('hombre/superior/nueva/', crear_prenda_superior_hombre, name='crear_prenda_superior_hombre'),
    path('hombre/superior/editar/<int:pk>/', editar_prenda_superior_hombre, name='editar_prenda_superior_hombre'),
    path('hombre/superior/eliminar/<int:pk>/', eliminar_prenda_superior_hombre, name='eliminar_prenda_superior_hombre'),
    path('armario/hombre/tren-inferior/', vista_tren_inferior_hombre, name='tren_inferior_hombre'),
    path('hombre/inferior/nueva/', crear_prenda_inferior_hombre, name='crear_prenda_inferior_hombre'),
    path('hombre/inferior/editar/<int:pk>/', editar_prenda_inferior_hombre, name='editar_prenda_inferior_hombre'),
    path('hombre/inferior/eliminar/<int:pk>/', eliminar_prenda_inferior_hombre, name='eliminar_prenda_inferior_hombre'),
    path('armario/hombre/calzado/', vista_calzado_hombre, name='calzado_hombre'),
    path('hombre/calzado/nueva/', crear_prenda_calzado_hombre, name='crear_prenda_calzado_hombre'),
    path('hombre/calzado/editar/<int:pk>/', editar_prenda_calzado_hombre, name='editar_prenda_calzado_hombre'),
    path('hombre/calzado/eliminar/<int:pk>/', eliminar_prenda_calzado_hombre, name='eliminar_prenda_calzado_hombre'),
]
