from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Empleado(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    cc: str
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_sangre: Optional[str] = None

    class Config:
        orm_mode = True

class EmpleadoUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    cc: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_sangre: Optional[str] = None

    class Config:
        orm_mode = True
