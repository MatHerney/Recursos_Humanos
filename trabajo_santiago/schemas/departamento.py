from pydantic import BaseModel
from typing import Optional

# Esquema para la creación de un nuevo departamento
class Departamento(BaseModel):
    nombre: str
    id_gerente: Optional[int] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema para la actualización de un departamento existente
class DepartamentoUpdate(BaseModel):
    nombre: Optional[str] = None
    id_gerente: Optional[int] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None

    class Config:
        orm_mode = True

