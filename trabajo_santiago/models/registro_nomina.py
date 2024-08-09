from sqlalchemy import Table, Column, Integer, Date, ForeignKey
from sqlalchemy.types import DECIMAL  
from config.db import meta, engine

# Definición de la tabla 'registro_nomina'
registro_nomina = Table(
    'registro_nomina', meta,
    Column('id_nomina', Integer, primary_key=True, autoincrement=True),
    Column('id_contrato', Integer, ForeignKey('contratos.id_contrato'), nullable=False),
    Column('fecha_pago', Date, nullable=True),
    Column('salario_base', DECIMAL(10, 2), nullable=True),
    Column('deducciones', DECIMAL(10, 2), nullable=True),
    Column('salario_neto', DECIMAL(10, 2), nullable=True),
    Column('id_periodo', Integer, ForeignKey('periodo_facturacion.id_periodo'), nullable=True)
)

# Creación de la tabla en la base de datos
try:
    meta.create_all(engine)
except Exception as e:
    print(f"Error al crear la tabla 'registro_nomina': {e}")


