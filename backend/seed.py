from db import SessionLocal, engine
from models import User, Incident, Base

def init_db():
    """
    Crea las tablas de la base de datos a partir de los modelos
    si no existen.
    """
    # 'engine' se importa desde db.py
    # 'Base' se importa desde models.py
    Base.metadata.create_all(bind=engine)

def seed_data():
    """
    Puebla la base de datos con datos de ejemplo.
    """
    # Crea una sesión de base de datos
    db = SessionLocal()
    
    try:
        # 1. Verificar si la base de datos ya tiene datos
        if db.query(User).first() is not None:
            print("La base de datos ya contiene datos. No se añadirán más.")
            return

        print("Poblando la base de datos con datos iniciales...")

        # 2. Crear Usuarios de ejemplo
        user1 = User(
            name="Ana García",
            email="ana.garcia@empresa.com"
        )
        user2 = User(
            name="Luis Martínez",
            email="luis.martinez@empresa.com"
        )
        user3 = User(
            name="Carla López",
            email="carla.lopez@empresa.com"
        )
        
        # Añadir usuarios a la sesión
        db.add_all([user1, user2, user3])
        
        # Guardar (commit) los usuarios en la BD
        # Hacemos commit aquí para que los usuarios obtengan sus IDs
        # y podamos asignarlos a las incidencias.
        db.commit()

        # 3. Crear Incidencias de ejemplo
        
        # Nota: Asignamos el 'owner' usando el objeto de usuario.
        # SQLAlchemy se encargará de asignar el 'id_user' automáticamente.
        
        inc1 = Incident(
            title="Impresora no funciona",
            description="La impresora del pasillo 2 no imprime.",
            status="abierta",
            owner=user1  # Asignado a Ana García
        )
        
        inc2 = Incident(
            title="Error en login",
            description="No puedo acceder al portal interno.",
            status="en_progreso",
            owner=user2  # Asignado a Luis Martínez
        )
        
        inc3 = Incident(
            title="Pantalla parpadea",
            description="El monitor de mi puesto (A-34) parpadea.",
            status="abierta",
            owner=user1  # También asignado a Ana García
        )
        
        inc4 = Incident(
            title="Solicitud de software",
            description="Necesito instalar Photoshop.",
            status="cerrada",
            owner=user3  # Asignado a Carla López
        )

        # Añadir incidencias a la sesión
        db.add_all([inc1, inc2, inc3, inc4])
        
        # Guardar (commit) las incidencias
        db.commit()

        print("Datos iniciales creados exitosamente.")

    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
        db.rollback() # Revertir cambios en caso de error
    finally:
        db.close() # Cerrar la sesión

if __name__ == "__main__":
    print("Inicializando la base de datos...")
    init_db()
    print("Base de datos inicializada.")
    
    # Poblar los datos
    seed_data()