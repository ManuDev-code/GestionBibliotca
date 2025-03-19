import os
import json
import datetime

# Clases para representar las entidades
class Usuario:
    ultimo_id = 0
    
    def __init__(self, id=None, nombre="", email="", telefono=""):
        if id is None:
            Usuario.ultimo_id += 1
            self.id = Usuario.ultimo_id
        else:
            self.id = id
            # Actualizar el último ID si el ID proporcionado es mayor
            if id > Usuario.ultimo_id:
                Usuario.ultimo_id = id
        
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
    
    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Email: {self.email} | Teléfono: {self.telefono}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            email=data.get("email"),
            telefono=data.get("telefono")
        )

class Libro:
    ultimo_id = 0
    
    def __init__(self, id=None, titulo="", autor="", isbn="", descripcion="", disponible=True):
        if id is None:
            Libro.ultimo_id += 1
            self.id = Libro.ultimo_id
        else:
            self.id = id
            # Actualizar el último ID si el ID proporcionado es mayor
            if id > Libro.ultimo_id:
                Libro.ultimo_id = id
        
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.descripcion = descripcion
        self.disponible = disponible
    
    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ID: {self.id} | Título: {self.titulo} | Autor: {self.autor} | ISBN: {self.isbn} | Estado: {estado}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "descripcion": self.descripcion,
            "disponible": self.disponible
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            titulo=data.get("titulo"),
            autor=data.get("autor"),
            isbn=data.get("isbn"),
            descripcion=data.get("descripcion"),
            disponible=data.get("disponible", True)
        )

class Prestamo:
    ultimo_id = 0
    
    def __init__(self, id=None, usuario_id=None, libro_id=None, fecha_prestamo=None, fecha_devolucion=None, devuelto=False):
        if id is None:
            Prestamo.ultimo_id += 1
            self.id = Prestamo.ultimo_id
        else:
            self.id = id
            # Actualizar el último ID si el ID proporcionado es mayor
            if id > Prestamo.ultimo_id:
                Prestamo.ultimo_id = id
        
        self.usuario_id = usuario_id
        self.libro_id = libro_id
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.datetime.now().strftime("%Y-%m-%d")
        self.fecha_devolucion = fecha_devolucion
        self.devuelto = devuelto
    
    def __str__(self):
        estado = "Devuelto" if self.devuelto else "Prestado"
        fecha_dev = self.fecha_devolucion if self.fecha_devolucion else "Pendiente"
        return f"ID: {self.id} | Usuario ID: {self.usuario_id} | Libro ID: {self.libro_id} | Fecha préstamo: {self.fecha_prestamo} | Fecha devolución: {fecha_dev} | Estado: {estado}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "libro_id": self.libro_id,
            "fecha_prestamo": self.fecha_prestamo,
            "fecha_devolucion": self.fecha_devolucion,
            "devuelto": self.devuelto
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            usuario_id=data.get("usuario_id"),
            libro_id=data.get("libro_id"),
            fecha_prestamo=data.get("fecha_prestamo"),
            fecha_devolucion=data.get("fecha_devolucion"),
            devuelto=data.get("devuelto", False)
        )

# Clase principal de la aplicación
class BibliotecaApp:
    def __init__(self):
        self.usuarios = []
        self.libros = []
        self.prestamos = []
        self.cargar_datos()
        self.cargar_contadores()
    
    # Métodos para cargar y guardar datos
    def cargar_datos(self):
        # Crear directorio de datos si no existe
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Cargar usuarios
        if os.path.exists("data/usuarios.json"):
            try:
                with open("data/usuarios.json", "r") as f:
                    usuarios_data = json.load(f)
                    self.usuarios = [Usuario.from_dict(u) for u in usuarios_data]
            except:
                print("Error al cargar usuarios. Se iniciará con una lista vacía.")
        
        # Cargar libros
        if os.path.exists("data/libros.json"):
            try:
                with open("data/libros.json", "r") as f:
                    libros_data = json.load(f)
                    self.libros = [Libro.from_dict(l) for l in libros_data]
            except:
                print("Error al cargar libros. Se iniciará con una lista vacía.")
        
        # Cargar préstamos
        if os.path.exists("data/prestamos.json"):
            try:
                with open("data/prestamos.json", "r") as f:
                    prestamos_data = json.load(f)
                    self.prestamos = [Prestamo.from_dict(p) for p in prestamos_data]
            except:
                print("Error al cargar préstamos. Se iniciará con una lista vacía.")
    
    def cargar_contadores(self):
        # Cargar contadores de IDs
        if os.path.exists("data/contadores.json"):
            try:
                with open("data/contadores.json", "r") as f:
                    contadores = json.load(f)
                    Usuario.ultimo_id = contadores.get("usuario_id", 0)
                    Libro.ultimo_id = contadores.get("libro_id", 0)
                    Prestamo.ultimo_id = contadores.get("prestamo_id", 0)
            except:
                print("Error al cargar contadores. Se usarán los valores por defecto.")
        else:
            # Si no existe el archivo, actualizar los contadores basados en los datos cargados
            if self.usuarios:
                Usuario.ultimo_id = max(u.id for u in self.usuarios)
            if self.libros:
                Libro.ultimo_id = max(l.id for l in self.libros)
            if self.prestamos:
                Prestamo.ultimo_id = max(p.id for p in self.prestamos)
    
    def guardar_datos(self):
        # Guardar usuarios
        with open("data/usuarios.json", "w") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4)
        
        # Guardar libros
        with open("data/libros.json", "w") as f:
            json.dump([l.to_dict() for l in self.libros], f, indent=4)
        
        # Guardar préstamos
        with open("data/prestamos.json", "w") as f:
            json.dump([p.to_dict() for p in self.prestamos], f, indent=4)
        
        # Guardar contadores
        with open("data/contadores.json", "w") as f:
            contadores = {
                "usuario_id": Usuario.ultimo_id,
                "libro_id": Libro.ultimo_id,
                "prestamo_id": Prestamo.ultimo_id
            }
            json.dump(contadores, f, indent=4)
    
    # Métodos para actualizar disponibilidad de libros
    def actualizar_disponibilidad_libros(self):
        # Primero marcar todos como disponibles
        for libro in self.libros:
            libro.disponible = True
        
        # Luego marcar como no disponibles los que están prestados
        for prestamo in self.prestamos:
            if not prestamo.devuelto:
                for libro in self.libros:
                    if libro.id == prestamo.libro_id:
                        libro.disponible = False
    
    # Métodos para gestión de usuarios
    def agregar_usuario(self, nombre, email, telefono):
        usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
        self.usuarios.append(usuario)
        self.guardar_datos()
        return usuario
    
    def buscar_usuario(self, termino):
        resultados = []
        termino = termino.lower()
        for usuario in self.usuarios:
            if (termino in usuario.nombre.lower() or 
                termino in usuario.email.lower() or 
                termino in str(usuario.id).lower() or
                termino in usuario.telefono.lower()):
                resultados.append(usuario)
        return resultados
    
    def obtener_usuario_por_id(self, id):
        for usuario in self.usuarios:
            if usuario.id == id:
                return usuario
        return None
    
    def actualizar_usuario(self, id, nombre, email, telefono):
        usuario = self.obtener_usuario_por_id(id)
        if usuario:
            usuario.nombre = nombre
            usuario.email = email
            usuario.telefono = telefono
            self.guardar_datos()
            return True
        return False
    
    def eliminar_usuario(self, id):
        usuario = self.obtener_usuario_por_id(id)
        if usuario:
            self.usuarios.remove(usuario)
            self.guardar_datos()
            return True
        return False
    
    # Métodos para gestión de libros
    def agregar_libro(self, titulo, autor, isbn, descripcion):
        libro = Libro(titulo=titulo, autor=autor, isbn=isbn, descripcion=descripcion)
        self.libros.append(libro)
        self.guardar_datos()
        return libro
    
    def buscar_libro(self, termino):
        resultados = []
        termino = termino.lower()
        for libro in self.libros:
            if (termino in libro.titulo.lower() or 
                termino in libro.autor.lower() or 
                termino in str(libro.id).lower() or
                termino in libro.isbn.lower()):
                resultados.append(libro)
        return resultados
    
    def obtener_libro_por_id(self, id):
        for libro in self.libros:
            if libro.id == id:
                return libro
        return None
    
    def actualizar_libro(self, id, titulo, autor, isbn, descripcion):
        libro = self.obtener_libro_por_id(id)
        if libro:
            libro.titulo = titulo
            libro.autor = autor
            libro.isbn = isbn
            libro.descripcion = descripcion
            self.guardar_datos()
            return True
        return False
    
    def eliminar_libro(self, id):
        libro = self.obtener_libro_por_id(id)
        if libro:
            self.libros.remove(libro)
            self.guardar_datos()
            return True
        return False
    
    # Métodos para gestión de préstamos
    def registrar_prestamo(self, usuario_id, libro_id, fecha_prestamo=None):
        # Verificar que el usuario existe
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            print("Error: Usuario no encontrado.")
            return None
        
        # Verificar que el libro existe y está disponible
        libro = self.obtener_libro_por_id(libro_id)
        if not libro:
            print("Error: Libro no encontrado.")
            return None
        
        if not libro.disponible:
            print("Error: El libro no está disponible.")
            return None
        
        # Crear el préstamo
        prestamo = Prestamo(
            usuario_id=usuario_id,
            libro_id=libro_id,
            fecha_prestamo=fecha_prestamo
        )
        
        self.prestamos.append(prestamo)
        
        # Actualizar disponibilidad del libro
        libro.disponible = False
        
        self.guardar_datos()
        return prestamo
    
    def devolver_libro(self, prestamo_id):
        for prestamo in self.prestamos:
            if prestamo.id == prestamo_id and not prestamo.devuelto:
                prestamo.devuelto = True
                prestamo.fecha_devolucion = datetime.datetime.now().strftime("%Y-%m-%d")
                self.actualizar_disponibilidad_libros()
                self.guardar_datos()
                return True
        return False
    
    def buscar_prestamo(self, termino):
        resultados = []
        termino = termino.lower()
        
        for prestamo in self.prestamos:
            usuario = self.obtener_usuario_por_id(prestamo.usuario_id)
            libro = self.obtener_libro_por_id(prestamo.libro_id)
            
            if usuario and libro:
                if (termino in usuario.nombre.lower() or 
                    termino in libro.titulo.lower() or
                    termino in str(prestamo.id).lower()):
                    resultados.append((prestamo, usuario, libro))
        
        return resultados
    
    def obtener_prestamo_por_id(self, id):
        for prestamo in self.prestamos:
            if prestamo.id == id:
                return prestamo
        return None
    
    def listar_prestamos_activos(self):
        activos = []
        for prestamo in self.prestamos:
            if not prestamo.devuelto:
                usuario = self.obtener_usuario_por_id(prestamo.usuario_id)
                libro = self.obtener_libro_por_id(prestamo.libro_id)
                if usuario and libro:
                    activos.append((prestamo, usuario, libro))
        return activos
    

# Funciones de utilidad para la interfaz de consola
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresiona Enter para continuar...")

def mostrar_titulo(titulo):
    limpiar_pantalla()
    print("=" * 60)
    print(f"{titulo:^60}")
    print("=" * 60)
    print()

def mostrar_menu(opciones, titulo):
    mostrar_titulo(titulo)
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    print("\n0. Volver")
    
    while True:
        try:
            seleccion = int(input("\nSelecciona una opción: "))
            if 0 <= seleccion <= len(opciones):
                return seleccion
            else:
                print("Opción no válida. Intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número.")
