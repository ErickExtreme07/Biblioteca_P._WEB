import redis
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    try:
        r = redis.Redis(
            host=os.getenv('KEYDB_HOST', 'localhost'),
            port=int(os.getenv('KEYDB_PORT', 6379)),
            db=int(os.getenv('KEYDB_DB', 0)),
            decode_responses=True # Para que nos devuelva strings y no bytes
        )
        r.ping() # Verificar conexión
        return r
    except redis.ConnectionError:
        print("❌ Error: No se pudo conectar a KeyDB. Verifica Docker.")
        return None