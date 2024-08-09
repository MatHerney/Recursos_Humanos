from pydantic import BaseModel
from typing import Optional
from datetime import date

# Esquema para la creación de un nuevo registro de asistencia
class RegistroAsistencia(BaseModel):
    id_empleado: int  # ID del empleado, campo obligatorio
    observaciones: Optional[str] = None  # Observaciones, campo opcional
    fecha: date  # Fecha de la asistencia, campo obligatorio
    id_periodo: Optional[int] = None  # ID del periodo de facturación, campo opcional

    class Config:
        orm_mode = True  # Habilita la compatibilidad con ORMs

# Esquema para la actualización de un registro de asistencia existente
class RegistroAsistenciaUpdate(BaseModel):
    id_empleado: Optional[int] = None  # ID del empleado, campo opcional
    observaciones: Optional[str] = None  # Observaciones, campo opcional
    fecha: Optional[date] = None  # Fecha de la asistencia, campo opcional
    id_periodo: Optional[int] = None  # ID del periodo de facturación, campo opcional

    class Config:
        orm_mode = True  # Habilita la compatibilidad con ORMs
