"""Compatibilidad temporal para imports históricos.

Los modelos pertenecen a ``productos`` y ``ventas``. Estas reexportaciones no
registran modelos en ``core`` y pueden retirarse cuando los consumidores
externos hayan actualizado sus imports.
"""

from productos.models import Producto
from ventas.models import DetallePedido, Pedido

__all__ = ['Producto', 'Pedido', 'DetallePedido']
