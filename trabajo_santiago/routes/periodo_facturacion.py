from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from config.db import conn
from models.periodo_facturacion import periodo_facturacion as periodo_facturacion_model
from schemas.periodo_facturacion import PeriodoFacturacion, PeriodoFacturacionUpdate

# Crear instancia de APIRouter
periodo_facturacion = APIRouter()

# Endpoint para obtener todos los periodos de facturación
@periodo_facturacion.get("/periodos")
def get_periodos():
    """
    Retorna la lista de todos los periodos de facturación.

    Returns:
        list: Lista de periodos de facturación.
    """
    try:
        result = conn.execute(periodo_facturacion_model.select()).fetchall()
        periodos_list = [dict(row._mapping) for row in result]
        return periodos_list
    except SQLAlchemyError as e:
        print(f"Error al obtener periodos de facturación: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener periodos de facturación")

# Endpoint para crear un nuevo periodo de facturación
@periodo_facturacion.post("/periodos")
def nuevo_periodo(periodo: PeriodoFacturacion):
    """
    Crea un nuevo periodo de facturación en la base de datos.

    Args:
        periodo (PeriodoFacturacion): Objeto periodo con los datos a insertar.

    Returns:
        dict: Mensaje de éxito y ID del periodo creado.
    """
    new_periodo = {
        "inicio_periodo": periodo.inicio_periodo,
        "final_periodo": periodo.final_periodo
    }

    try:
        result = conn.execute(periodo_facturacion_model.insert().values(new_periodo))
        conn.commit()  # Confirmar la transacción
        return {"message": "Periodo de facturación creado exitosamente", "id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        conn.rollback()  # Deshacer la transacción en caso de error
        print(f"Error al crear el periodo de facturación: {e}")
        raise HTTPException(status_code=400, detail="Error al crear el periodo de facturación")

# Endpoint para actualizar un periodo de facturación existente
@periodo_facturacion.put("/periodos/{id_periodo}")
def actualizar_periodo(id_periodo: int, periodo_update: PeriodoFacturacionUpdate):
    """
    Actualiza los datos de un periodo de facturación existente.

    Args:
        id_periodo (int): ID del periodo de facturación a actualizar.
        periodo_update (PeriodoFacturacionUpdate): Objeto con los datos a actualizar.

    Returns:
        dict: Mensaje de éxito.
    """
    try:
        # Buscar el periodo por su ID
        periodo = conn.execute(periodo_facturacion_model.select().where(periodo_facturacion_model.c.id_periodo == id_periodo)).first()
        if not periodo:
            raise HTTPException(status_code=404, detail="Periodo de facturación no encontrado")

        # Crear un diccionario de los campos a actualizar
        update_data = periodo_update.dict(exclude_unset=True)

        # Actualizar los datos en la base de datos
        conn.execute(
            periodo_facturacion_model.update()
            .where(periodo_facturacion_model.c.id_periodo == id_periodo)
            .values(**update_data)
        )
        conn.commit()
        return {"message": "Periodo de facturación actualizado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al actualizar el periodo de facturación: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el periodo de facturación")

# Endpoint para eliminar un periodo de facturación
@periodo_facturacion.delete("/periodos/{id_periodo}")
def eliminar_periodo(id_periodo: int):
    """
    Elimina un periodo de facturación de la base de datos.

    Args:
        id_periodo (int): ID del periodo de facturación a eliminar.

    Returns:
        dict: Mensaje de éxito o error.
    """
    try:
        # Buscar el periodo por su ID
        periodo = conn.execute(periodo_facturacion_model.select().where(periodo_facturacion_model.c.id_periodo == id_periodo)).first()
        if not periodo:
            raise HTTPException(status_code=404, detail="Periodo de facturación no encontrado")

        # Eliminar el periodo de la base de datos
        conn.execute(periodo_facturacion_model.delete().where(periodo_facturacion_model.c.id_periodo == id_periodo))
        conn.commit()
        return {"message": "Periodo de facturación eliminado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al eliminar el periodo de facturación: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el periodo de facturación")
