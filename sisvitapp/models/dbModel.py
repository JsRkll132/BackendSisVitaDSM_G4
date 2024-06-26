from sqlalchemy import Float, create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, CheckConstraint, Index
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref
import os
from dotenv import load_dotenv
# Crear la base declarativa
Base = declarative_base()
load_dotenv()
# Definir la clase Usuarios
class Usuarios(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        CheckConstraint("tipo_usuario IN ('paciente', 'psicologo')", name='check_tipo_usuario'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(255), nullable=False)
    apellido_paterno = Column(String(255), nullable=False)
    apellido_materno = Column(String(255), nullable=False)
    correo = Column(String(255), unique=True, nullable=False)
    numero_celular = Column(String(20), nullable=False)
    nombre_usuario = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    tipo_usuario = Column(String(10), nullable=False)
    ubigeo = Column(String(6), ForeignKey('ubigeo.ubigeo'), nullable=True) 
    # Relaciones
    paciente = relationship("Pacientes", backref=backref("usuario", uselist=False), cascade="all, delete", passive_deletes=True)
    psicologo = relationship("Psicologos", backref=backref("usuario", uselist=False), cascade="all, delete", passive_deletes=True)
class Ubigeo(Base):
    __tablename__ = 'ubigeo'
    ubigeo = Column(String(6), primary_key=True)
    distrito = Column(String(255), nullable=False)
    provincia = Column(String(255), nullable=False)
    departamento = Column(String(255), nullable=False)
    poblacion = Column(Integer, nullable=False)
    superficie = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)

    # Relación con la tabla Usuarios
    usuarios = relationship("Usuarios", backref="ubicacion")
# Definir la clase Pacientes
class Pacientes(Base):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), unique=True, nullable=False)

# Definir la clase Psicologos
class Psicologos(Base):
    __tablename__ = 'psicologos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), unique=True, nullable=False)

# Definir la clase Formularios
class Formularios(Base):
    __tablename__ = 'formularios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(255), nullable=False)
    descripcion = Column(Text)

    # Relaciones
    preguntas = relationship("Preguntas", backref="formulario", cascade="all, delete", passive_deletes=True)
    diagnosticos = relationship("Diagnosticos", backref="formulario", cascade="all, delete", passive_deletes=True)

# Definir la clase Preguntas
class Preguntas(Base):
    __tablename__ = 'preguntas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    formulario_id = Column(Integer, ForeignKey('formularios.id', ondelete='CASCADE'), nullable=False)
    pregunta = Column(Text, nullable=False)

    # Relaciones
   #respuestas = relationship("Respuestas", backref="pregunta", cascade="all, delete", passive_deletes=True)

# Definir la clase Respuestas
class Respuestas(Base):
    __tablename__ = 'respuestas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pregunta_id = Column(Integer, ForeignKey('preguntas.id', ondelete='CASCADE'), nullable=False)
    paciente_id = Column(Integer, ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    respuesta = Column(Text, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    completado_formulario_id = Column(Integer, ForeignKey('completadoformulario.id', ondelete='CASCADE'), nullable=False)
    puntuacion = Column(Integer,nullable=True)
    completado_formulario = relationship("CompletadoFormulario", backref="respuesta", cascade="all, delete", passive_deletes=True)
    pacientes = relationship("Pacientes", backref="respuesta", cascade="all, delete", passive_deletes=True)
    preguntas = relationship("Preguntas", backref="respuesta", cascade="all, delete", passive_deletes=True)
# Definir la clase Diagnosticos
class Diagnosticos(Base):
    __tablename__ = 'diagnosticos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    psicologo_id = Column(Integer, ForeignKey('psicologos.id', ondelete='CASCADE'), nullable=False)
    formulario_id = Column(Integer, ForeignKey('formularios.id', ondelete='CASCADE'), nullable=False)
    completado_formulario_id = Column(Integer, ForeignKey('completadoformulario.id', ondelete='CASCADE'), nullable=True)
    calificacion = Column(Integer, nullable=False)
    diagnostico = Column(Text, nullable=False)
    fecha_diagnostico = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    
    completado_formulario = relationship("CompletadoFormulario", backref="diagnosticos", cascade="all, delete", passive_deletes=True)


class ContenidoFormulario(Base):
    __tablename__ = 'contenidoformulario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    respuestaformulario = Column(String(255), nullable=False)
    puntaje = Column(Integer, nullable=False)
    formulario_id = Column(Integer, ForeignKey('formularios.id'), nullable=False)
    formulario = relationship("Formularios", backref="contenidoformulario")

class CompletadoFormulario(Base):
    __tablename__ = 'completadoformulario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    formulario_id = Column(Integer, ForeignKey('formularios.id'), nullable=False)
    fecha_completado = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
    nivel_ansiedad = Column(String(255),nullable=True)
    Pacientes = relationship("Pacientes", backref="completadoformulario_", cascade="all, delete", passive_deletes=True)
    Formularios = relationship("Formularios", backref="completadoformulario_", cascade="all, delete", passive_deletes=True)
# Crear índices para las tablas Respuestas y Diagnosticos
Index('idx_respuestas_paciente_id', Respuestas.paciente_id)
Index('idx_respuestas_pregunta_id', Respuestas.pregunta_id)
Index('idx_diagnosticos_paciente_id', Diagnosticos.paciente_id)
Index('idx_diagnosticos_psicologo_id', Diagnosticos.psicologo_id)
Index('idx_diagnosticos_formulario_id', Diagnosticos.formulario_id)

# Configurar la base de datos (ajusta la cadena de conexión según tus necesidades)
print(os.getenv('DATABASE_URL'))
engine = create_engine(os.getenv('DATABASE_URL'))

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
