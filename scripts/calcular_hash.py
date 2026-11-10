import hashlib

def obtener_sha256(ruta_fichero):
    sha = hashlib.sha256()
    with open(ruta_fichero, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

# Comprobación de integridad para los archivos de la práctica
print("Hash SHA-256 (Original):", obtener_sha256("datos/telemetria_envios.csv"))
print("Hash SHA-256 (Limpio):  ", obtener_sha256("datos/telemetria_limpia.csv"))