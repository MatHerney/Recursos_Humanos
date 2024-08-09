from fastapi import FastAPI
from routes.empleados import empleados
from routes.contratos import contratos
from routes.departamentos import departamentos
from routes.evaluacion_desempeno import evaluacion_desempeno
from routes.periodo_facturacion import periodo_facturacion
from routes.registro_asistencia import registro_asistencia
from routes.registro_nomina import registro_nomina

# Crear instancia de FastAPI
app = FastAPI()

# Incluir routers con prefijos y tags para mejor organización
app.include_router(periodo_facturacion, prefix="/periodo-facturacion", tags=["Periodo de Facturación"])
app.include_router(empleados, prefix="/empleados", tags=["Empleados"])
app.include_router(departamentos, prefix="/departamentos", tags=["Departamentos"])
app.include_router(contratos, prefix="/contratos", tags=["Contratos"])
app.include_router(evaluacion_desempeno, prefix="/evaluacion-desempeno", tags=["Evaluación de Desempeño"])
app.include_router(registro_asistencia, prefix="/registro-asistencia", tags=["Registro de Asistencia"])
app.include_router(registro_nomina, prefix="/registro-nomina", tags=["Registro de Nómina"])

# Ruta de inicio
@app.get("/", tags=["Home"])
async def read_root():
    """
    Retorna un mensaje de bienvenida.

    Returns:
        dict: Mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de Recursos Humanos"}
