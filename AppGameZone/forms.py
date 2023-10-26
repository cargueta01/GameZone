from django import forms
from .models import BalanceComprobacion, RegistroTransaccion, Inventario

class BalanceForm(forms.ModelForm):
    class Meta:
        model = BalanceComprobacion
        fields = ['fechaDeBalance']
        widgets ={
            'fechaDeBalance' : forms.DateInput(format='%d/%m/%Y'),
        }

class RegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroTransaccion
        fields = ['fechaDeRegistro']
        widgets ={
            'fechaDeRegistro' : forms.DateInput(format='%d/%m/%Y')
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['fechaDeRegistroDeOperacion']
