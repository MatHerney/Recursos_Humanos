from sqlalchemy import Table, Column, Integer, Date
from config.db import meta, engine

# Definición de la tabla 'periodo_facturacion'
periodo_facturacion = Table(
    'periodo_facturacion', meta,
    Column('id_periodo', Integer, primary_key=True, autoincrement=True),
    Column('inicio_periodo', Date, nullable=False),
    Column('final_periodo', Date, nullable=False)
)

# Creación de la tabla en la base de datos
try:
    meta.create_all(engine)
except Exception as e:
    print(f"Error al crear la tabla 'periodo_facturacion': {e}")
