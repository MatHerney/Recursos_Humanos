from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class EvaluacionDesempeno(BaseModel):
    id_empleado: int
    id_periodo: int
    calificacion: Optional[Decimal] = None

    class Config:
        orm_mode = True

class EvaluacionDesempenoUpdate(BaseModel):
    id_empleado: Optional[int] = None
    id_periodo: Optional[int] = None
    calificacion: Optional[Decimal] = None

    class Config:
        orm_mode = True
