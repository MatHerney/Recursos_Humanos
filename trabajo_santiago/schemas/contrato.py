from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class Contrato(BaseModel):
    id_empleado: Optional[int] = None
    id_departamento: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    tipo_contrato: Optional[str] = None
    cargo: Optional[str] = None
    salario_base: Optional[Decimal] = None
    email_empresarial: Optional[str] = None
    fecha_desvinculacion: Optional[date] = None
    eps: Optional[str] = None
    arl: Optional[str] = None
    pensiones: Optional[str] = None

    class Config:
        orm_mode = True

class ContratoUpdate(BaseModel):
    id_departamento: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    tipo_contrato: Optional[str] = None
    cargo: Optional[str] = None
    salario_base: Optional[Decimal] = None
    email_empresarial: Optional[str] = None
    fecha_desvinculacion: Optional[date] = None
    eps: Optional[str] = None
    arl: Optional[str] = None
    pensiones: Optional[str] = None

    class Config:
        orm_mode = True
