from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('Cat_Cuentas/', views.Catalogo_Cuenta, name='Cat_cuentas'),
    path('Reg_Transaccion/', views.transaccion, name='reg_transaccion'),
    path('FormLibroMayor/', views.formlibromayor, name='FormLibroMayor'),
    path('LibroMayor/', views.libromayor, name='LibroMayor'),
    path('BalComprobacion/', views.balance, name='Balance'),
    path('ManoDeObra/', views.manodeobra, name='ManoDeObra'),
    path('Inventarios/', views.Inventario_a, name='Inventario'),
    path('CierreContable/', views.cierrecontable, name='Cierrecontable'),
    path('Costeo/', views.costeo, name='Costeo'),
]