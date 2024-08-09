from sqlalchemy import Table, Column, Integer, Text, ForeignKey, Date
from config.db import meta, engine

# Definición de la tabla 'registro_asistencia'
registro_asistencia = Table(
    'registro_asistencia', meta,
    Column('id_asistencia', Integer, primary_key=True, autoincrement=True),
    Column('id_empleado', Integer, ForeignKey('empleados.id_empleado'), nullable=False),
    Column('observaciones', Text, nullable=True),
    Column('fecha', Date, nullable=False),
    Column('id_periodo', Integer, ForeignKey('periodo_facturacion.id_periodo'), nullable=True)
)

# Creación de la tabla en la base de datos
try:
    meta.create_all(engine)
except Exception as e:
    print(f"Error al crear la tabla 'registro_asistencia': {e}")
