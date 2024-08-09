from sqlalchemy import Table, Column, Integer, String, ForeignKey
from config.db import meta, engine

# Definición de la tabla 'departamentos'
departamentos = Table(
    'departamentos', meta,
    Column('id_departamento', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(100), nullable=False),
    Column('id_gerente', Integer, ForeignKey('empleados.id_empleado'), nullable=True),
    Column('correo', String(100), nullable=True),
    Column('telefono', String(20), nullable=True)
)

# Creación de la tabla en la base de datos
try:
    meta.create_all(engine)
except Exception as e:
    print(f"Error al crear la tabla 'departamentos': {e}")
