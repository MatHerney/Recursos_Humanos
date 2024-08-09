from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from config.db import conn
from models.registro_asistencia import registro_asistencia as registro_asistencia_model
from schemas.registro_asistencia import RegistroAsistencia, RegistroAsistenciaUpdate

# Crear instancia de APIRouter
registro_asistencia = APIRouter()

# Endpoint para obtener todos los registros de asistencia
@registro_asistencia.get("/registro_asistencia")
def get_registro_asistencia():
    """
    Retorna la lista de todos los registros de asistencia.

    Returns:
        list: Lista de registros de asistencia.
    """
    try:
        result = conn.execute(registro_asistencia_model.select()).fetchall()
        registros_list = [dict(row._mapping) for row in result]
        return registros_list
    except SQLAlchemyError as e:
        print(f"Error al obtener registros de asistencia: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener registros de asistencia")

# Endpoint para crear un nuevo registro de asistencia
@registro_asistencia.post("/registro_asistencia")
def nuevo_registro_asistencia(registro: RegistroAsistencia):
    """
    Crea un nuevo registro de asistencia en la base de datos.

    Args:
        registro (RegistroAsistencia): Objeto registro con los datos a insertar.

    Returns:
        dict: Mensaje de éxito y ID del registro creado.
    """
    new_registro = {
        "id_empleado": registro.id_empleado,
        "observaciones": registro.observaciones,
        "fecha": registro.fecha,
        "id_periodo": registro.id_periodo
    }

    try:
        result = conn.execute(registro_asistencia_model.insert().values(new_registro))
        conn.commit()
        return {"message": "Registro de asistencia creado exitosamente", "id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al crear el registro de asistencia: {e}")
        raise HTTPException(status_code=400, detail="Error al crear el registro de asistencia")

# Endpoint para actualizar un registro de asistencia existente
@registro_asistencia.put("/registro_asistencia/{id_asistencia}")
def actualizar_registro_asistencia(id_asistencia: int, registro_update: RegistroAsistenciaUpdate):
    """
    Actualiza los datos de un registro de asistencia existente.

    Args:
        id_asistencia (int): ID del registro de asistencia a actualizar.
        registro_update (RegistroAsistenciaUpdate): Objeto con los datos a actualizar.

    Returns:
        dict: Mensaje de éxito.
    """
    try:
        registro = conn.execute(registro_asistencia_model.select().where(registro_asistencia_model.c.id_asistencia == id_asistencia)).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")

        update_data = registro_update.dict(exclude_unset=True)

        conn.execute(
            registro_asistencia_model.update()
            .where(registro_asistencia_model.c.id_asistencia == id_asistencia)
            .values(**update_data)
        )
        conn.commit()
        return {"message": "Registro de asistencia actualizado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al actualizar el registro de asistencia: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el registro de asistencia")

# Endpoint para eliminar un registro de asistencia
@registro_asistencia.delete("/registro_asistencia/{id_asistencia}")
def eliminar_registro_asistencia(id_asistencia: int):
    """
    Elimina un registro de asistencia de la base de datos.

    Args:
        id_asistencia (int): ID del registro de asistencia a eliminar.

    Returns:
        dict: Mensaje de éxito o error.
    """
    try:
        registro = conn.execute(registro_asistencia_model.select().where(registro_asistencia_model.c.id_asistencia == id_asistencia)).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")

        conn.execute(registro_asistencia_model.delete().where(registro_asistencia_model.c.id_asistencia == id_asistencia))
        conn.commit()
        return {"message": "Registro de asistencia eliminado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al eliminar el registro de asistencia: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el registro de asistencia")
