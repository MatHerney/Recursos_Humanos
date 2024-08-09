from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from config.db import conn
from models.evaluacion_desempeno import evaluacion_desempeno as evaluacion_desempeno_model
from schemas.evaluacion_desempeno import EvaluacionDesempeno, EvaluacionDesempenoUpdate

# Crear instancia de APIRouter
evaluacion_desempeno = APIRouter()

# Endpoint para obtener todas las evaluaciones de desempeño
@evaluacion_desempeno.get("/evaluacion_desempeno")
def get_evaluaciones():
    """
    Retorna la lista de todas las evaluaciones de desempeño.

    Returns:
        list: Lista de evaluaciones de desempeño.
    """
    try:
        result = conn.execute(evaluacion_desempeno_model.select()).fetchall()
        evaluaciones_list = [dict(row._mapping) for row in result]
        return evaluaciones_list
    except SQLAlchemyError as e:
        print(f"Error al obtener evaluaciones de desempeño: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener evaluaciones de desempeño")

# Endpoint para crear una nueva evaluación de desempeño
@evaluacion_desempeno.post("/evaluacion_desempeno")
def nueva_evaluacion(evaluacion: EvaluacionDesempeno):
    """
    Crea una nueva evaluación de desempeño en la base de datos.

    Args:
        evaluacion (EvaluacionDesempeno): Objeto evaluación con los datos a insertar.

    Returns:
        dict: Mensaje de éxito y ID de la evaluación creada.
    """
    new_evaluacion = {
        "id_empleado": evaluacion.id_empleado,
        "id_periodo": evaluacion.id_periodo,
        "calificacion": evaluacion.calificacion
    }

    try:
        result = conn.execute(evaluacion_desempeno_model.insert().values(new_evaluacion))
        conn.commit()
        return {"message": "Evaluación de desempeño creada exitosamente", "id": result.inserted_primary_key[0]}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al crear la evaluación de desempeño: {e}")
        raise HTTPException(status_code=400, detail="Error al crear la evaluación de desempeño")

# Endpoint para actualizar una evaluación de desempeño existente
@evaluacion_desempeno.put("/evaluacion_desempeno/{id_evaluacion}")
def actualizar_evaluacion(id_evaluacion: int, evaluacion_update: EvaluacionDesempenoUpdate):
    """
    Actualiza los datos de una evaluación de desempeño existente.

    Args:
        id_evaluacion (int): ID de la evaluación a actualizar.
        evaluacion_update (EvaluacionDesempenoUpdate): Objeto con los datos a actualizar.

    Returns:
        dict: Mensaje de éxito.
    """
    try:
        evaluacion = conn.execute(evaluacion_desempeno_model.select().where(evaluacion_desempeno_model.c.id_evaluacion == id_evaluacion)).first()
        if not evaluacion:
            raise HTTPException(status_code=404, detail="Evaluación de desempeño no encontrada")

        update_data = evaluacion_update.dict(exclude_unset=True)

        conn.execute(
            evaluacion_desempeno_model.update()
            .where(evaluacion_desempeno_model.c.id_evaluacion == id_evaluacion)
            .values(**update_data)
        )
        conn.commit()
        return {"message": "Evaluación de desempeño actualizada exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al actualizar la evaluación de desempeño: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar la evaluación de desempeño")

# Endpoint para eliminar una evaluación de desempeño
@evaluacion_desempeno.delete("/evaluacion_desempeno/{id_evaluacion}")
def eliminar_evaluacion(id_evaluacion: int):
    """
    Elimina una evaluación de desempeño de la base de datos.

    Args:
        id_evaluacion (int): ID de la evaluación a eliminar.

    Returns:
        dict: Mensaje de éxito o error.
    """
    try:
        evaluacion = conn.execute(evaluacion_desempeno_model.select().where(evaluacion_desempeno_model.c.id_evaluacion == id_evaluacion)).first()
        if not evaluacion:
            raise HTTPException(status_code=404, detail="Evaluación de desempeño no encontrada")

        conn.execute(evaluacion_desempeno_model.delete().where(evaluacion_desempeno_model.c.id_evaluacion == id_evaluacion))
        conn.commit()
        return {"message": "Evaluación de desempeño eliminada exitosamente"}
    except SQLAlchemyError as e:
        conn.rollback()
        print(f"Error al eliminar la evaluación de desempeño: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar la evaluación de desempeño")
