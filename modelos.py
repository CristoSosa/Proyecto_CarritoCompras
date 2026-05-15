from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]
    nombre: str
    contrasena: bytes
    correo: str
    numero: str


@dataclass
class Empleado:
    id: Optional[int]
    nombre: str
    contrasena: bytes
    correo: str
    numero: str
    nomina: float


@dataclass
class Categoria:
    id: Optional[int]
    nombre: str
    descripcion: str


@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    precio: float
    cantidad: int
    categoria_id: int


@dataclass
class ArticuloCarrito:
    id: int
    usuario_id: int
    producto_id: int
    nombre_producto: str
    precio: float
    cantidad: int
    categoria: str

    @property
    def subtotal(self):
        return self.precio * self.cantidad


@dataclass
class Venta:
    id: int
    usuario: str
    producto: str
    total: float


@dataclass
class Sesion:
    id: int
    nombre: str
    tipo: str
