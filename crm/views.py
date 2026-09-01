from django.shortcuts import render

def dashboard_view(request):
    context = {
        'total_clientes': 128,
        'clientes_activos': 96,
        'interacciones': 48,
        'clientes_en_riesgo': 15,
    }
    return render(request, 'crm/dashboard.html', context)

def clientes_view(request):
    lista_clientes = [
        {'id': '001', 'nombre': 'María López', 'empresa': 'Cliente Frecuente', 'correo': 'maria@email.com', 'telefono': '449-123-4567', 'etapa': 'Frecuente', 'estado': 'Activo'},
        {'id': '002', 'nombre': 'Juan Pérez', 'empresa': 'Botanas Jerez', 'correo': 'juan.p@email.com', 'telefono': '449-987-6543', 'etapa': 'Activo', 'estado': 'Activo'},
        {'id': '003', 'nombre': 'Ana García', 'empresa': 'Eventos Zacatecas', 'correo': 'ana.garcia@email.com', 'telefono': '449-555-0192', 'etapa': 'Prospecto', 'estado': 'Activo'},
        {'id': '004', 'nombre': 'Carlos Ruiz', 'empresa': 'Particular', 'correo': 'carlos.ruiz@email.com', 'telefono': '449-333-8899', 'etapa': 'Inactivo', 'estado': 'Inactivo'},
        {'id': '005', 'nombre': 'Luis Morales', 'empresa': 'Cervecería Local', 'correo': 'luis@email.com', 'telefono': '449-777-4411', 'etapa': 'Frecuente', 'estado': 'Activo'},
    ]
    context = {'clientes': lista_clientes}
    return render(request, 'crm/clientes.html', context)

def detalle_cliente_view(request, cliente_id):
    # Simulamos los datos del cliente seleccionado
    cliente = {
        'id': cliente_id,
        'nombre': 'María López',
        'empresa': 'Cliente Frecuente - El Camarón Crudo',
        'correo': 'maria@email.com',
        'telefono': '449-123-4567',
        'fecha_registro': '10/01/2026',
        'etapa': 'Frecuente',
        'estado': 'Activo'
    }
    
    # Historial de interacciones (Timeline requerido por la profesora)
    interacciones = [
        {'tipo': 'Llamada', 'fecha': '15/08/2026', 'descripcion': 'Se confirmó pedido de tostilocos y se habló sobre próximos productos de temporada.', 'usuario': 'Admin'},
        {'tipo': 'Correo', 'fecha': '10/08/2026', 'descripcion': 'Se envió información y menú actualizado de litros de aguachile y ceviche.', 'usuario': 'Admin'},
        {'tipo': 'Reunión', 'fecha': '02/08/2026', 'descripcion': 'Reunión en sucursal para revisar opciones de servicio para evento especial.', 'usuario': 'Admin'},
    ]

    context = {
        'cliente': cliente,
        'interacciones': interacciones
    }
    return render(request, 'crm/detalle_cliente.html', context)