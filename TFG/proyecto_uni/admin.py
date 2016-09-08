# -*- coding: utf-8 -*-

# Copyright 2016 Alvaro Feal 
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

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
