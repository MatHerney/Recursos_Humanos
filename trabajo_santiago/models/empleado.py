from sqlalchemy import Table, Column, Integer, String, Date
from config.db import meta, engine

# Definición de la tabla 'empleados'
empleados = Table(
    'empleados', meta,
    Column('id_empleado', Integer, primary_key=True, autoincrement=True),
    Column('nombres', String(100), nullable=False),
    Column('apellidos', String(100), nullable=False),
    Column('cc', String(50), unique=True, nullable=False),
    Column('fecha_nacimiento', Date, nullable=False),
    Column('direccion', String(200), nullable=True),
    Column('telefono', String(20), nullable=True),
    Column('email', String(100), nullable=True),
    Column('tipo_sangre', String(10), nullable=True)
)

# Creación de la tabla en la base de datos
try:
    meta.create_all(engine)
except Exception as e:
    print(f"Error al crear la tabla 'empleados': {e}")
