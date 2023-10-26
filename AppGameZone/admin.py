from django.contrib import admin
from AppGameZone.models import CatalogoCuenta, RegistroTransaccion, LibroMayor, Inventario, CierreContable

admin.site.register(CatalogoCuenta)
admin.site.register(RegistroTransaccion)
admin.site.register(LibroMayor)
admin.site.register(Inventario)
admin.site.register(CierreContable)