from pydantic import BaseModel
from typing import Optional
from datetime import date

# Esquema para la creación de un nuevo periodo de facturación
class PeriodoFacturacion(BaseModel):
    inicio_periodo: date  # Fecha de inicio del periodo, campo obligatorio
    final_periodo: date  # Fecha de finalización del periodo, campo obligatorio

    class Config:
        orm_mode = True  # Habilita la compatibilidad con ORMs

# Esquema para la actualización de un periodo de facturación existente
class PeriodoFacturacionUpdate(BaseModel):
    inicio_periodo: Optional[date] = None  # Fecha de inicio del periodo, campo opcional
    final_periodo: Optional[date] = None  # Fecha de finalización del periodo, campo opcional

    class Config:
        orm_mode = True  # Habilita la compatibilidad con ORMs
