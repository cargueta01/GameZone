from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CatalogoCuenta, LibroMayor, RegistroTransaccion, Inventario


# cuentas que existen segun su categoria en el catalogo de cuentas
catalogo = {
    'Activo': {'1101': 'Caja', '1102': 'Inventario', '1103': 'IVA crédito fiscal',
               '1201': 'Mobiliario', '1202': 'Pago anticipado de local', '1203': 'Equipo de computo'},

    'Pasivo': {'2101': 'IVA débito fiscal'},

    'Capital': {'3101': 'Capital contable'},

    'Gastos': {'4101': 'Compras', '4102': 'Gasto de venta', '4103': 'Descuento sobre venta',
               '4104': 'Devoluciones sobre venta', '4105': 'Pago de servicios básicos',  '4106': 'Pago de empleados',
               '4107': 'Gastos sobre compras'},

    'Ingresos': {'5101': 'Devoluciones sobre compra', '5102': 'Descuento sobre compra', '5103': 'Ventas'}
}


def buscar_clave_por_valor(diccionario, valor_buscar):
    for elemento, sub_diccionario in diccionario.items():
        for clave, valor in sub_diccionario.items():
            if valor == valor_buscar:
                return clave
    return None


def inicio(request):
    return render(request, 'home.html')
# Create your views here.


def Catalogo_Cuenta(request):

    return render(request, "Cat_Cuentas.html")


def transaccion(request):

    valorCuentas = catalogo['Gastos']
    print("esto es el valor de las cuentas: " + str(valorCuentas))
    libros = LibroMayor.objects.all()

    if request.method == 'POST':
        libroseleccionado = request.POST.get('libroSeleccionado')
        tipoDeCuenta = request.POST.get('tipoDeCuenta')
        cuenta = request.POST.get('cuenta')
        codigoCatalogo = buscar_clave_por_valor(catalogo, cuenta)
        libroGuardar = libros.get(nombreLibro=libroseleccionado)
        tipoDeMonto = request.POST.get('tipoDeMonto')
        fechaDeRegistro = request.POST.get('fechaDeRegistro')
        monto = request.POST.get('montoTransaccion')
        descripcion = request.POST.get('descripcion')
        print("este es el codigo del catalogo " + str(codigoCatalogo))

        cat = CatalogoCuenta.objects.create(
            tipoDeCuenta=tipoDeCuenta, nombreDeCuenta=cuenta, codigo=codigoCatalogo)
        RegistroTransaccion.objects.create(fechaDeRegistro=fechaDeRegistro, tipoDeMonto=tipoDeMonto,
                                           montoTransaccion=monto, descripcion=descripcion, registroCatalogo=cat,
                                           registroLibro=libroGuardar)
    mensaje = ""
    return render(request, "Reg_Transaccion.html", {'valorCuentas': valorCuentas,
                                                    'libros': libros, 'mensaje': mensaje}
                  )


def formlibromayor(request):
    if request.method == 'POST':
        nombreLibro = request.POST.get('nombreLibro')
        fechaApertura = request.POST.get('fechaApertura')
        fechaCierre = request.POST.get('fechaCierre')
        LibroMayor.objects.create(
            nombreLibro=nombreLibro, fechaDeApertura=fechaApertura, fechaDeCierre=fechaCierre)
        print("\nse creo el libro mayor\n")
    return render(request, "Form_LibroMayor.html")


def libromayor(request):
    # cuentas y sumas inicializadas en null
    cuentas = None
    sumas = None
    # todas las nombreDeCuenta de la clase CatalogoCuenta
    # lista = CatalogoCuenta.objects.values_list('nombreDeCuenta', flat=True)

    # buscar en RegistroTransaccion por registroLibro
    cuentas = RegistroTransaccion.objects.filter(registroLibro=1)

    # consultar todos los libros mayores
    libros = LibroMayor.objects.all()
    libroTitulo = None
    if request.method == 'POST':
        libroSeleccionado = request.POST.get('libroSeleccionado')
        print("este es el el id: " + str(libroSeleccionado))
        cuentas = RegistroTransaccion.objects.filter(
            registroLibro=libroSeleccionado)

        libroTitulo = LibroMayor.objects.get(idLibro=libroSeleccionado)

    # diccionario con sumas
    sumas = {}
    tipos = ['Activo', 'Pasivo', 'Capital', 'Gastos', 'Ingresos']
    for i in tipos:
        # estos son los nombres de las cuentas
        lista = list(catalogo[i].values())
        # print("esto es ")
        # print(lista)
        for j in lista:
            debe = 0
            haber = 0
            for c in cuentas:
                if c.registroCatalogo.nombreDeCuenta == j:
                    if c.tipoDeMonto == 'Debe':
                        debe += c.montoTransaccion
                    elif c.tipoDeMonto == 'Haber':
                        haber += c.montoTransaccion
            new_key = j.replace(' ', '_')
            if i == 'Activo' or i == 'Gastos':
                sumas[new_key] = abs(debe - haber)
                # print("esta es la lista: "+ str(j)+" y su debe : "+str(sumas[new_key]))
            else:
                sumas[new_key] = abs(haber - debe)

        # print("estos son los resultados:\n" + str(sumas))
        # print("\nesta es una cuenta:" + str(sumas['Inventario']))

    return render(request, "Lib_Mayor.html", {'cuentas': cuentas, 'sumas': sumas, 'libros': libros,
                                              'titulo': libroTitulo})

def balance(request):
    debeTotal = 0
    haberTotal = 0
    sumas = None
    libros = LibroMayor.objects.all()
    libroTitulo = None
    if request.method == 'POST':

        #devuelve la llave foranea, osea el id del libro
        libroSeleccionado = request.POST.get('libroSeleccionado')
        cuentas = RegistroTransaccion.objects.filter(registroLibro=libroSeleccionado)
        sumas = {}
        tipos = ['Activo', 'Pasivo', 'Capital', 'Gastos', 'Ingresos']
        for i in tipos:
            # estos son los nombres de las cuentas
            lista = list(catalogo[i].values())
            # print("esto es ")
            # print(lista)
            for j in lista:
                debe = 0
                haber = 0
                for c in cuentas:
                    if c.registroCatalogo.nombreDeCuenta == j:
                        if c.tipoDeMonto == 'Debe':
                            debe += c.montoTransaccion
                            
                        elif c.tipoDeMonto == 'Haber':
                            haber += c.montoTransaccion
                            
                new_key = j.replace(' ', '_')
                if i == 'Activo' or i == 'Gastos':
                    sumas[new_key] = abs(debe - haber)
                    debeTotal += sumas[new_key]
                    # print("esta es la lista: "+ str(j)+" y su debe : "+str(sumas[new_key]))
                else:
                    sumas[new_key] = abs(haber - debe)
                    haberTotal += sumas[new_key]
                    
            libroTitulo = LibroMayor.objects.get(idLibro=libroSeleccionado)
            libroTitulo.saldoDeudor = debeTotal
            libroTitulo.saldoAcreedor = haberTotal
            libroTitulo.save()
    print("estos son los debe y haber totales:\n" + str(debeTotal) + " " + str(haberTotal))
    return render(request, "Bal_Comprob.html", {'sumas': sumas, 'libros': libros, 'titulo': libroTitulo,
                                                'debeTotal': debeTotal, 'haberTotal': haberTotal})

def cierrecontable(request):
    cuentas = None
    sumas = None
    libroSeleccionado = None
    # todas las nombreDeCuenta de la clase CatalogoCuenta
    # lista = CatalogoCuenta.objects.values_list('nombreDeCuenta', flat=True)

    # buscar en RegistroTransaccion por registroLibro
    cuentas = RegistroTransaccion.objects.filter(registroLibro=1)

    # consultar todos los libros mayores
    libros = LibroMayor.objects.all()
    libroTitulo = None
    if request.method == 'POST':
        libroSeleccionado = request.POST.get('libroSeleccionado')
        print("este es el el id: " + str(libroSeleccionado))
        cuentas = RegistroTransaccion.objects.filter(
            registroLibro=libroSeleccionado)

        libroTitulo = LibroMayor.objects.get(idLibro=libroSeleccionado)

    # diccionario con sumas
    sumas = {}
    tipos = ['Activo', 'Pasivo', 'Capital', 'Gastos', 'Ingresos']
    for i in tipos:
        # estos son los nombres de las cuentas
        lista = list(catalogo[i].values())
        # print("esto es ")
        # print(lista)
        for j in lista:
            debe = 0
            haber = 0
            for c in cuentas:
                if c.registroCatalogo.nombreDeCuenta == j:
                    if c.tipoDeMonto == 'Debe':
                        debe += c.montoTransaccion
                    elif c.tipoDeMonto == 'Haber':
                        haber += c.montoTransaccion
            new_key = j.replace(' ', '_')
            if i == 'Activo' or i == 'Gastos':
                sumas[j] = abs(debe - haber)
                # print("esta es la lista: "+ str(j)+" y su debe : "+str(sumas[new_key]))
            else:
                sumas[j] = abs(haber - debe)
    
    contador = 0
    inventarioInicial = 0
    busqueda = RegistroTransaccion.objects.filter(registroLibro=libroSeleccionado)
    for i in busqueda:
        if i.registroCatalogo.nombreDeCuenta == 'Inventario' and contador == 0 and i.tipoDeMonto == 'Debe':
            print("este es el inventario: " + str(i.montoTransaccion))
            inventarioInicial = i.montoTransaccion
            contador += 1
        else:
            inventarioInicial = 0

    print("esta es mi busqueda: " + str(inventarioInicial))

    ventas_netas = sumas['Ventas'] - sumas['Devoluciones sobre venta'] - sumas['Descuento sobre venta']

    compras_netas = sumas['Compras'] - sumas['Devoluciones sobre compra'] - sumas['Descuento sobre compra']

    compras_totales = compras_netas + sumas['Gastos sobre compras']

    mercancias_disponibles = compras_netas + inventarioInicial

    costo_de_ventas = mercancias_disponibles - sumas['Inventario']

    return render(request, "Cierre_Cont.html",{ 'libros': libros, 'ventas_netas': ventas_netas, 
                            'compras_netas': compras_netas, 'compras_totales': compras_totales, 
                            'mercancias_disponibles': mercancias_disponibles, 'costo_de_ventas': costo_de_ventas,
                            'titulo': libroTitulo})

def manodeobra(request):

    return render(request, "Mano_Obra.html")

def Inventario_a(request):
    try:
        if request.method == 'POST':
            fechaMovimiento = request.POST.get('fechaMovimiento')
            tipoMovimiento = request.POST.get('tipoMovimiento')
            cantidadMaterial = int(request.POST.get('cantidadMaterial'))
            precioUnitario = request.POST.get('precioUnitario')
            descripcion = request.POST.get('descripcion')

            entradas = Inventario.objects.filter(tipoDeMovimiento='Entrada').order_by("fechaDeMovimiento")
            entradas = entradas.reverse()
            #print(f"esta es la cantidad de material {cantidadMaterial} y esta la cantidad de producto {entradas[1].residuo}" )
            if len(entradas) > 0 and tipoMovimiento == 'Salida':
                for a in entradas:
                    #supon que la cantidadMaterial es 590
                    #print("estas son las salidas: " + str(a.cantidadProducto))

                    if cantidadMaterial == a.residuo:
                        residuo = 0
                        a.residuo = 0   
                        a.save()
                        Inventario.objects.create(fechaDeMovimiento=fechaMovimiento, tipoDeMovimiento =tipoMovimiento,
                                                cantidadProducto=cantidadMaterial, costoUnitario= a.costoUnitario,
                                                descripcionInventario=descripcion, residuo = residuo,
                                                montoValor = (a.costoUnitario*cantidadMaterial), saldoValor = residuo*a.costoUnitario)
                        print(f"la cantidad de material es igual a la cantidad de producto {cantidadMaterial} == {a.cantidadProducto}")
                        break
                    
                    elif cantidadMaterial > a.residuo and a.residuo > 0:
                        residuo = cantidadMaterial - a.residuo

                        Inventario.objects.create(fechaDeMovimiento=fechaMovimiento, tipoDeMovimiento =tipoMovimiento,
                                                cantidadProducto=(cantidadMaterial-residuo), costoUnitario= a.costoUnitario,
                                                descripcionInventario=descripcion, residuo = 0, 
                                                montoValor = (a.costoUnitario*(cantidadMaterial-residuo)), saldoValor = 0)
                        cantidadMaterial = residuo
                        a.residuo = 0
                        a.save()
                        continue
                    elif cantidadMaterial < a.residuo and a.residuo > 0: 
                        residuo = a.residuo - cantidadMaterial
                        a.residuo = residuo
                        a.save()
                        Inventario.objects.create(fechaDeMovimiento=fechaMovimiento, tipoDeMovimiento =tipoMovimiento,
                                                cantidadProducto=cantidadMaterial, costoUnitario= a.costoUnitario,
                                                descripcionInventario=descripcion, residuo = residuo,
                                                montoValor = (a.costoUnitario*cantidadMaterial), saldoValor = residuo*a.costoUnitario)
                        break
            elif tipoMovimiento == 'Entrada':    
                if precioUnitario != '':
                    precioUnitario = float(precioUnitario)
                    #crear aqui objeto de entrada
                    Inventario.objects.create(fechaDeMovimiento=fechaMovimiento, tipoDeMovimiento =tipoMovimiento,
                                              cantidadProducto=cantidadMaterial, costoUnitario=precioUnitario,
                                              descripcionInventario=descripcion, residuo = cantidadMaterial,
                                              montoValor = (precioUnitario*cantidadMaterial), saldoValor = (cantidadMaterial*precioUnitario))
            inventario = Inventario.objects.all().order_by("fechaDeMovimiento")
            return render(request, "Inventario.html",{'inventario': inventario})
        else:
            entradaTotal = 0
            salidaTotal = 0
            saldoTotal = 0   
            inventario = Inventario.objects.all().order_by("fechaDeMovimiento")
            for i in inventario:
                if i.tipoDeMovimiento == 'Entrada':
                    if i.saldoValor is not None:
                        entradaTotal += i.saldoValor
                    if i.residuo is not None and i.costoUnitario is not None:
                        saldoTotal += i.residuo * i.costoUnitario
                elif i.tipoDeMovimiento == 'Salida':
                    if i.montoValor is not None:
                        salidaTotal += i.montoValor
            return render(request, "Inventario.html",{'inventario': inventario, 'entradaTotal': entradaTotal, 
                                                    'salidaTotal': salidaTotal, 'saldoTotal': saldoTotal})
    except Exception as e:
        print((f"\neste es el error {e}\n"))
        return render(request, "Inventario.html")

def costeo(request):

    return render(request, "Costeo.html")
