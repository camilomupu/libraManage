from sqlalchemy import Column, Double, Integer, String, ForeignKey, Date, LargeBinary
from sqlalchemy.orm import relationship
from config.db import Base


# usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    correo = Column(String(100), unique=True)
    contrasena = Column(String(100))
    fechaNacimiento = Column(Date)
    id_rol = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("Rol", back_populates="usuario")

    informe = relationship("Informe", back_populates="usuario")

    compraLibro = relationship("CompraLibro", back_populates="usuario")

    prestamo = relationship("Prestamo", back_populates="usuario")


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))

    usuario = relationship("Usuario", back_populates="rol")


class Informe(Base):
    __tablename__ = "informes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fechaGeneracion = Column(Date)
    numeroLibrosPrestados = Column(Integer)
    numeroLibrosNoDevueltos = Column(Integer)
    numeroComprasLibros = Column(Integer)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="informe")


# libros


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))

    libroDigital = relationship("LibroDigital", back_populates="categoria")
    libroFisico = relationship("LibroFisico", back_populates="categoria")


class SubCategoria(Base):
    __tablename__ = "subCategorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))

    libroDigital = relationship("LibroDigital", back_populates="subCategoria")
    libroFisico = relationship("LibroFisico", back_populates="subCategoria")


class Autor(Base):
    __tablename__ = "autores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))

    libroDigital = relationship("LibroDigital", back_populates="autor")
    libroFisico = relationship("LibroFisico", back_populates="autor")


# libroDigital


class LibroDigital(Base):
    __tablename__ = "librosDigitales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100))
    portada = Column(String(100), nullable=False)
    link_Libro = Column(String(100), nullable=False)
    descripcion = Column(String(100))
    precio = Column(Double)
    id_autor = Column(Integer, ForeignKey("autores.id"))
    id_subcategoria = Column(Integer, ForeignKey("subCategorias.id"))
    id_categoria = Column(Integer, ForeignKey("categorias.id"))

    autor = relationship("Autor", back_populates="libroDigital")
    subCategoria = relationship("SubCategoria", back_populates="libroDigital")
    categoria = relationship("Categoria", back_populates="libroDigital")

    compraLibro = relationship("CompraLibro", back_populates="libroDigital")


class CompraLibro(Base):
    __tablename__ = "comprasLibros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_libroDigital = Column(Integer, ForeignKey("librosDigitales.id"))

    usuario = relationship("Usuario", back_populates="compraLibro")
    libroDigital = relationship("LibroDigital", back_populates="compraLibro")


# LibroFisico
class LibroFisico(Base):
    __tablename__ = "librosFisicos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100))
    descripcion = Column(String(100))
    portada = Column(String(100), nullable=False)
    ubicacion = Column(String(100))
    #imagen = Column(LargeBinary, nullable=True)
    estado = Column(String(100))
    id_autor = Column(Integer, ForeignKey("autores.id"))
    id_subcategoria = Column(Integer, ForeignKey("subCategorias.id"))
    id_categoria = Column(Integer, ForeignKey("categorias.id"))

    autor = relationship("Autor", back_populates="libroFisico")
    subCategoria = relationship("SubCategoria", back_populates="libroFisico")
    categoria = relationship("Categoria", back_populates="libroFisico")

    prestamo = relationship("Prestamo", back_populates="libroFisico")


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fechaPrestamo = Column(Date)
    fechaVencimiento = Column(Date)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    id_libroFisico = Column(Integer, ForeignKey("librosFisicos.id"))

    usuario = relationship("Usuario", back_populates="prestamo")
    libroFisico = relationship("LibroFisico", back_populates="prestamo")
    multa = relationship("Multa", back_populates="prestamo")


class Multa(Base):
    __tablename__ = "multas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valorDeuda = Column(Double)
    fechaDePago = Column(Date)
    estadoMulta = Column(Integer)
    id_prestamo = Column(Integer, ForeignKey("prestamos.id"))

    prestamo = relationship("Prestamo", back_populates="multa")
