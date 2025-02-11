from django.contrib import admin
from .models import Espacio, ProyectoConstruccion, Cliente, Evaluacion, Sugerencia

admin.site.register(Espacio)
admin.site.register(ProyectoConstruccion)
admin.site.register(Cliente)
admin.site.register(Evaluacion)
admin.site.register(Sugerencia)