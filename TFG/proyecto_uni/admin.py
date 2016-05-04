from django.contrib import admin

# Register your models here.
from .models import Asignaturas
from .models import Centros
from .models import ImpartidaEn
from .models import Encuestas
from .models import Tasas
from .models import Titulaciones 
#Register your models here.

admin.site.register(Asignaturas)
admin.site.register(Centros)
admin.site.register(ImpartidaEn)
admin.site.register(Encuestas)
admin.site.register(Tasas)
admin.site.register(Titulaciones)
