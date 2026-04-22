{
    'name': 'Sale Order Line to Stock Move Lot',
    'version': '17.0.1.0.0',
    'summary': 'Asigna lotes desde la línea de venta a la transferencia de inventario',
    'description': """
        Este módulo permite:
        - Seleccionar un lote en las líneas de la orden de venta (filtrado por disponibilidad en stock.quant).
        - Propagar automáticamente el lote seleccionado a la operación detallada (stock.move.line) del albarán de entrega o recepción asociado.
    """,
    'category': 'Sales/Sales',
    'author': 'Tu Empresa / Tu Nombre',
    'website': 'https://www.tudominio.com',
    'depends': [
        'sale_management', 
        'stock',
        'sale_stock', # Crucial para el campo sale_line_id en stock.move
    ],
    'data': [
        # Recuerda agregar aquí tu archivo XML donde inyectas el campo lot_id a la vista sale.view_order_form
        # 'views/sale_order_views.xml', 
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}