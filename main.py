from fastapi import FastAPI
import os
import sqlite3

app = FastAPI()
DB_FILE = os.path.join(".", "data", "db.sqlite3")

# Función para crear la tabla si no existe
def create_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS access_count (endpoint TEXT PRIMARY KEY, count INTEGER)"
    )
    conn.commit()
    conn.close()

# Función para incrementar el contador
def increment_count(endpoint):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO access_count VALUES (?, 0)", (endpoint,))
    c.execute("UPDATE access_count SET count = count + 1 WHERE endpoint = ?", (endpoint,))
    conn.commit()
    conn.close()

@app.get("/")
async def root():
    return {"message": "¡Hola! ingresa a /docs para ver la documentación."}

# Ruta de ejemplo
@app.get("/example")
async def example():
    increment_count("example")
    return {"message": "¡Hola! Has accedido al endpoint /example."}

@app.get("/new2")
async def new2():
    increment_count("new2")
    return {"message": "¡Hola! Has accedido al endpoint /new2."}

# Ruta para obtener el contador de un endpoint
@app.get("/count/{endpoint}")
async def count(endpoint: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT count FROM access_count WHERE endpoint = ?", (endpoint,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"endpoint": endpoint, "count": result[0]}
    else:
        return {"endpoint": endpoint, "count": 0}

# Crea la tabla al iniciar la aplicación
create_table()
