from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class RegistroNomina(BaseModel):
    id_nomina: Optional[int] = None
    id_contrato: int
    fecha_pago: Optional[date] = None
    salario_base: Optional[Decimal] = None
    deducciones: Optional[Decimal] = None
    salario_neto: Optional[Decimal] = None
    id_periodo: Optional[int] = None

    class Config:
        orm_mode = True

class RegistroNominaUpdate(BaseModel):
    id_contrato: Optional[int] = None
    fecha_pago: Optional[date] = None
    salario_base: Optional[Decimal] = None
    deducciones: Optional[Decimal] = None
    salario_neto: Optional[Decimal] = None
    id_periodo: Optional[int] = None

    class Config:
        orm_mode = True
