import json
import uuid
from database_keydb import obtener_conexion

def agregar_libro(titulo, autor, genero, estado):
    db = obtener_conexion()
    if db:
        libro_id = str(uuid.uuid4())[:8] # Generamos un ID corto único
        libro_data = {
            "id": libro_id,
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        }
        # Guardamos con la clave libro:<id>
        db.set(f"libro:{libro_id}", json.dumps(libro_data))
        return libro_id

def ver_libros():
    db = obtener_conexion()
    libros = []
    if db:
        # Buscamos todas las llaves que empiecen con "libro:"
        keys = db.keys("libro:*")
        for key in keys:
            libros.append(json.loads(db.get(key)))
    return libros

def actualizar_libro(id_libro, campo, nuevo_valor):
    db = obtener_conexion()
    if db:
        key = f"libro:{id_libro}"
        data = db.get(key)
        if data:
            libro = json.loads(data)
            libro[campo] = nuevo_valor
            db.set(key, json.dumps(libro))
            return True
    return False

def eliminar_libro(id_libro):
    db = obtener_conexion()
    if db:
        return db.delete(f"libro:{id_libro}")

def buscar_libros(clave, valor):
    todos = ver_libros()
    # Filtramos en Python ya que KeyDB es clave-valor simple
    return [l for l in todos if valor.lower() in str(l.get(clave, "")).lower()]