from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_
from config.db import conn
from models.empleado import empleados as empleados_model
from models.contrato import contratos as contratos_model
from schemas.contrato import Contrato, ContratoUpdate
from typing import Optional
# Crear instancia de APIRouter
contratos = APIRouter()

# Endpoint para obtener todos los contratos
@contratos.get("/contratos")
def get_contratos():
    """
    Retorna la lista de todos los contratos.

    Returns:
        list: Lista de contratos.
    """
    try:
        result = conn.execute(contratos_model.select()).fetchall()
        contratos_list = [dict(row._mapping) for row in result]
        return contratos_list
    except SQLAlchemyError as e:
        print(f"Error al obtener contratos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener contratos")

# Endpoint para crear un nuevo contrato
@contratos.post("/nuevo_contrato")
def contrato_nuevo(cc: str, contrato: Contrato):
    """
    Crea un nuevo contrato en la base de datos asociado a un empleado.

    Args:
        cc (str): Número de cédula del empleado asociado al contrato.
        contrato (Contrato): Objeto contrato con los datos a insertar.

    Returns:
        dict: Mensaje de éxito y ID del contrato creado.
    """
    try:
        # Buscar el empleado por su número de cédula
        empleado = conn.execute(empleados_model.select().where(empleados_model.c.cc == cc)).first()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # Asociar el contrato al ID del empleado encontrado
        new_contrato = contrato.dict(exclude_unset=True)  # Excluir campos no establecidos
        new_contrato['id_empleado'] = empleado.id_empleado

        result = conn.execute(contratos_model.insert().values(new_contrato))
        conn.commit()  # Confirmar la transacción
        return {"message": "Contrato creado exitosamente", "id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        conn.rollback()  # Deshacer la transacción en caso de error
        print(f"Error al crear el contrato: {e}")
        raise HTTPException(status_code=400, detail="Error al crear el contrato")

# Endpoint para actualizar un contrato existente
@contratos.put("/contratos/{id_contrato}")
def actualizar_contrato(id_contrato: int, contrato_update: ContratoUpdate):
    """
    Actualiza los datos de un contrato existente.

    Args:
        id_contrato (int): ID del contrato a actualizar.
        contrato_update (ContratoUpdate): Objeto con los datos a actualizar.

    Returns:
        dict: Mensaje de éxito.
    """
    try:
        # Buscar el contrato por su ID
        contrato = conn.execute(contratos_model.select().where(contratos_model.c.id_contrato == id_contrato)).first()
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")

        # Crear un diccionario de los campos a actualizar
        update_data = contrato_update.dict(exclude_unset=True)

        # Actualizar los datos en la base de datos
        conn.execute(
            contratos_model.update()
            .where(contratos_model.c.id_contrato == id_contrato)
            .values(**update_data)
        )
        conn.commit()
        return {"message": "Contrato actualizado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al actualizar el contrato: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el contrato")

# Endpoint para eliminar un contrato
@contratos.delete("/contratos/{id_contrato}")
def eliminar_contrato(id_contrato: int):
    """
    Elimina un contrato de la base de datos.

    Args:
        id_contrato (int): ID del contrato a eliminar.

    Returns:
        dict: Mensaje de éxito o error.
    """
    try:
        # Buscar el contrato por su ID
        contrato = conn.execute(contratos_model.select().where(contratos_model.c.id_contrato == id_contrato)).first()
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")

        # Eliminar el contrato de la base de datos
        conn.execute(contratos_model.delete().where(contratos_model.c.id_contrato == id_contrato))
        conn.commit()
        return {"message": "Contrato eliminado exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al eliminar el contrato: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el contrato")





# Endpoint para obtener los contratos históricos de un empleado por ID o CC
@contratos.get("/contratos/historico")
def obtener_contratos_historicos(id_empleado: Optional[int] = None, cc: Optional[str] = None):
    """
    Retorna los contratos históricos de un empleado especificado por ID o número de cédula (cc).

    Args:
        id_empleado (int, opcional): ID del empleado.
        cc (str, opcional): Número de cédula del empleado.

    Returns:
        list: Lista de contratos históricos del empleado.
    """
    try:
        # Verificar que se haya proporcionado al menos un criterio de búsqueda
        if id_empleado is None and cc is None:
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un criterio de búsqueda (id_empleado o cc)")

        # Buscar el empleado por su ID o cédula
        query = empleados_model.select()
        if id_empleado is not None and cc is not None:
            query = query.where(and_(empleados_model.c.id_empleado == id_empleado, empleados_model.c.cc == cc))
        elif id_empleado is not None:
            query = query.where(empleados_model.c.id_empleado == id_empleado)
        elif cc is not None:
            query = query.where(empleados_model.c.cc == cc)

        empleado = conn.execute(query).first()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        # Obtener los contratos históricos del empleado
        contratos_query = contratos_model.select().where(contratos_model.c.id_empleado == empleado.id_empleado)
        result = conn.execute(contratos_query).fetchall()
        contratos_list = [dict(row._mapping) for row in result]
        return contratos_list
    except SQLAlchemyError as e:
        print(f"Error al obtener los contratos históricos del empleado: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los contratos históricos del empleado")





