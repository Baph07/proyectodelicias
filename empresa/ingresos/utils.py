from decimal import Decimal

PRECIOS_HELADOS = {
    'Barquilla sencilla': Decimal('2.00'),
    'Barquilla doble': Decimal('2.50'),
    'Barquillón': Decimal('2.80'),
    'Mini Cesta': Decimal('1.80'),
    'Cesta': Decimal('2.80'),
    'Tina sencilla': Decimal('1.50'),
    'Tina doble': Decimal('2.30'),
}

PRECIOS_POSTRES = {
    ('Tortas', 'Completa Medio Kilo'): Decimal('12.00'),
    ('Tortas', 'Completa Kilo'): Decimal('25.00'),
    ('Tortas', 'Porción'): Decimal('3.00'),
    ('Quesillo', 'Completo'): Decimal('20.00'),
    ('Quesillo', 'Porción'): Decimal('3.00'),
    ('Yogurt', 'Pequeño'): Decimal('2.20'),
    ('Yogurt', 'Mediano'): Decimal('3.60'),
    ('Yogurt', 'Grande'): Decimal('5.00'),
}

PRECIOS_OTROS = {
    'Refresco litro y medio': Decimal('1.80'),
    'Chupeta': Decimal('0.18'),
    'Chesito': Decimal('0.20'),
    'Q-citos': Decimal('0.30'),
    'Caramelo lokiño': Decimal('0.10'),
    'Galleta María': Decimal('0.15'),
    'Galleta rellena': Decimal('0.35'),
}

def obtener_precio_unitario(producto):
    if producto['categoria'] == 'Helados':
        return PRECIOS_HELADOS.get(producto['tipo_helado'], Decimal('0'))

    if producto['categoria'] == 'Postres':
        clave = (producto['tipo_postre'], producto['tamaño'])
        return PRECIOS_POSTRES.get(clave, Decimal('0'))

    if producto['categoria'] == 'Otros':
        return PRECIOS_OTROS.get(producto['nombre'], Decimal('0'))

    return Decimal('0')
