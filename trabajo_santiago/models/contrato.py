from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.types import DECIMAL
from config.db import meta, engine, conn

# Definición de la tabla 'contratos'
contratos = Table(
    'contratos', meta,
    Column('id_contrato', Integer, primary_key=True, autoincrement=True),
    Column('id_empleado', Integer, ForeignKey('empleados.id_empleado'), nullable=False),
    Column('id_departamento', Integer, ForeignKey('departamentos.id_departamento'), nullable=True),
    Column('fecha_inicio', Date, nullable=True),
    Column('fecha_fin', Date, nullable=True),
    Column('tipo_contrato', String(50), nullable=True),
    Column('cargo', String(100), nullable=True),
    Column('salario_base', DECIMAL(10, 2), nullable=True),
    Column('email_empresarial', String(100), nullable=True),
    Column('fecha_desvinculacion', Date, nullable=True),
    Column('eps', String(100), nullable=True),
    Column('arl', String(100), nullable=True),
    Column('pensiones', String(100), nullable=True)
)

# Creación de la tabla en la base de datos
try:
    meta.create_all(engine)
except Exception as e:
    print(f"Error al crear la tabla 'contratos': {e}")

