from django.contrib import admin
from .models import TipoCuerpo, Evento, Lugar

admin.site.register(TipoCuerpo)
admin.site.register(Evento)
admin.site.register(Lugar)

from .models import CategoriaSuperiorMujer, PrendaSuperiorMujer, CategoriaInferiorMujer, PrendaInferiorMujer, CategoriaCalzadoMujer, PrendaCalzadoMujer
from .models import CategoriaSuperiorHombre, PrendaSuperiorHombre, CategoriaInferiorHombre, PrendaInferiorHombre, CategoriaCalzadoHombre, PrendaCalzadoHombre

 
admin.site.register(CategoriaSuperiorMujer)
admin.site.register(PrendaSuperiorMujer)


admin.site.register(CategoriaInferiorMujer)
admin.site.register(PrendaInferiorMujer)

admin.site.register(CategoriaCalzadoMujer)
admin.site.register(PrendaCalzadoMujer)


admin.site.register(CategoriaSuperiorHombre)
admin.site.register(PrendaSuperiorHombre)

admin.site.register(CategoriaInferiorHombre)
admin.site.register(PrendaInferiorHombre)

admin.site.register(CategoriaCalzadoHombre)
admin.site.register(PrendaCalzadoHombre)