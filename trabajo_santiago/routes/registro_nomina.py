from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from config.db import conn
from models.empleado import empleados as empleados_model
from models.contrato import contratos as contratos_model
from models.registro_nomina import registro_nomina as registro_nomina_model
from models.periodo_facturacion import periodo_facturacion as periodo_facturacion_model
from schemas.registro_nomina import RegistroNomina, RegistroNominaUpdate
from fastapi.responses import HTMLResponse
from typing import Optional
from datetime import date, datetime

# Crear instancia de APIRouter
registro_nomina = APIRouter()

# Endpoint para obtener todos los registros de nómina
@registro_nomina.get("/registro_nomina")
def get_registro_nomina():
    """
    Retorna la lista de todos los registros de nómina.

    Returns:
        list: Lista de registros de nómina.
    """
    try:
        result = conn.execute(registro_nomina_model.select()).fetchall()
        registros_list = [dict(row._mapping) for row in result]
        return registros_list
    except SQLAlchemyError as e:
        print(f"Error al obtener registros de nómina: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener registros de nómina")

# Endpoint para crear un nuevo registro de nómina
@registro_nomina.post("/registro_nomina")
def nuevo_registro_nomina(registro: RegistroNomina):
    """
    Crea un nuevo registro de nómina en la base de datos.

    Args:
        registro (RegistroNomina): Objeto registro con los datos a insertar.

    Returns:
        dict: Mensaje de éxito y ID del registro creado.
    """
    new_registro = {
        "id_contrato": registro.id_contrato,
        "fecha_pago": registro.fecha_pago,
        "salario_base": registro.salario_base,
        "deducciones": registro.deducciones,
        "salario_neto": registro.salario_neto,
        "id_periodo": registro.id_periodo
    }

    try:
        result = conn.execute(registro_nomina_model.insert().values(new_registro))
        conn.commit()
        return {"message": "Registro de nómina creado exitosamente", "id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al crear el registro de nómina: {e}")
        raise HTTPException(status_code=400, detail="Error al crear el registro de nómina")

# Endpoint para actualizar un registro de nómina existente
@registro_nomina.put("/registro_nomina/{id_nomina}")
def actualizar_registro_nomina(id_nomina: int, registro_update: RegistroNominaUpdate):
    """
    Actualiza los datos de un registro de nómina existente.

    Args:
        id_nomina (int): ID del registro de nómina a actualizar.
        registro_update (RegistroNominaUpdate): Objeto con los datos a actualizar.

    Returns:
        dict: Mensaje de éxito.
    """
    try:
        registro = conn.execute(registro_nomina_model.select().where(registro_nomina_model.c.id_nomina == id_nomina)).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de nómina no encontrado")

        update_data = registro_update.dict(exclude_unset=True)

        conn.execute(
            registro_nomina_model.update()
            .where(registro_nomina_model.c.id_nomina == id_nomina)
            .values(**update_data)
        )
        conn.commit()
        return {"message": "Registro de nómina actualizado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al actualizar el registro de nómina: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el registro de nómina")

# Endpoint para eliminar un registro de nómina
@registro_nomina.delete("/registro_nomina/{id_nomina}")
def eliminar_registro_nomina(id_nomina: int):
    """
    Elimina un registro de nómina de la base de datos.

    Args:
        id_nomina (int): ID del registro de nómina a eliminar.

    Returns:
        dict: Mensaje de éxito o error.
    """
    try:
        registro = conn.execute(registro_nomina_model.select().where(registro_nomina_model.c.id_nomina == id_nomina)).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de nómina no encontrado")

        conn.execute(registro_nomina_model.delete().where(registro_nomina_model.c.id_nomina == id_nomina))
        conn.commit()
        return {"message": "Registro de nómina eliminado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al eliminar el registro de nómina: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el registro de nómina")

# Endpoint para obtener la colilla de pago de un empleado
@registro_nomina.get("/colilla_pago", response_class=HTMLResponse)
def obtener_colilla_pago(cc: str, fecha: Optional[date] = None, id_periodo: Optional[int] = None):
    """
    Genera la colilla de pago de un empleado especificado por cédula (cc) y
    una fecha específica o el ID del período de facturación.

    Args:
        cc (str): Número de cédula del empleado.
        fecha (date, opcional): Fecha específica dentro del período de facturación.
        id_periodo (int, opcional): ID del período de facturación.

    Returns:
        str: Colilla de pago en formato HTML.
    """
    try:
        if fecha is None and id_periodo is None:
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un criterio de búsqueda (fecha o id_periodo)")

        empleado = conn.execute(empleados_model.select().where(empleados_model.c.cc == cc)).first()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        if fecha:
            periodo = conn.execute(
                periodo_facturacion_model.select().where(
                    and_(
                        periodo_facturacion_model.c.inicio_periodo <= fecha,
                        periodo_facturacion_model.c.final_periodo >= fecha
                    )
                )
            ).first()
            if not periodo:
                raise HTTPException(status_code=404, detail="Período de facturación no encontrado para la fecha proporcionada")
            id_periodo = periodo.id_periodo
        else:
            periodo = conn.execute(periodo_facturacion_model.select().where(periodo_facturacion_model.c.id_periodo == id_periodo)).first()
            if not periodo:
                raise HTTPException(status_code=404, detail="Período de facturación no encontrado")

        contrato = conn.execute(
            contratos_model.select().where(
                (contratos_model.c.id_empleado == empleado.id_empleado) &
                (contratos_model.c.fecha_desvinculacion == None)
            )
        ).first()
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato activo no encontrado")

        registro_nomina = conn.execute(
            registro_nomina_model.select().where(
                (registro_nomina_model.c.id_contrato == contrato.id_contrato) &
                (registro_nomina_model.c.id_periodo == id_periodo)
            ).order_by(registro_nomina_model.c.fecha_pago.desc())
        ).first()
        if not registro_nomina:
            raise HTTPException(status_code=404, detail="Registro de nómina no encontrado para el período de facturación")

        html_content = f"""
        <html>
        <head>
            <title>Colilla de Pago</title>
        </head>
        <body>
            <h1>Colilla de Pago</h1>
            <p><strong>Nombres:</strong> {empleado.nombres}</p>
            <p><strong>Apellidos:</strong> {empleado.apellidos}</p>
            <p><strong>Cédula:</strong> {empleado.cc}</p>
            <p><strong>Cargo:</strong> {contrato.cargo}</p>
            <p><strong>Salario Base:</strong> {registro_nomina.salario_base}</p>
            <p><strong>Deducciones:</strong> {registro_nomina.deducciones}</p>
            <p><strong>Salario Neto:</strong> {registro_nomina.salario_neto}</p>
            <p><strong>Fecha de Consulta:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Período de Facturación:</strong> {periodo.inicio_periodo} a {periodo.final_periodo}</p>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except SQLAlchemyError as e:
        print(f"Error al generar la colilla de pago: {e}")
        raise HTTPException(status_code=500, detail="Error al generar la colilla de pago")
