import pandas as pd
import hashlib

def obtener_sha256(ruta_fichero):
    """Calcula la firma SHA-256 en formato binario."""
    sha = hashlib.sha256()
    with open(ruta_fichero, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

def depurar_datos(ruta_entrada, ruta_salida):
    print("=== PASO 1: CARGA DE DATOS Y HASH INICIAL ===")
    df = pd.read_csv(ruta_entrada)
    filas_iniciales = len(df)
    hash_inicial = obtener_sha256(ruta_entrada)
    print(f"Filas leídas: {filas_iniciales}")
    print(f"SHA-256 Original: {hash_inicial}\n")

    print("=== PASO 2: APLICACIÓN DE REGLAS DE CALIDAD ===")

    # Regla 1: Deduplicación (Eliminar registros exactos o con mismo ID y timestamp)
    df = df.drop_duplicates(subset=['id_envio', 'timestamp_lectura'])
    print(f"Filas tras eliminar duplicados: {len(df)}")

    # Regla 2: Tratamiento de Nulos (Campos obligatorios de la telemetría)
    df = df.dropna(subset=['peso_kg', 'temp_celsius', 'destino'])
    print(f"Filas tras eliminar valores nulos (NaN): {len(df)}")

    # Regla 3: Outliers / Inconsistencias de Peso (El peso debe ser positivo)
    df = df[df['peso_kg'] > 0]
    print(f"Filas tras eliminar pesos negativos: {len(df)}")

    # Regla 4: Outliers de Temperatura (Rango operativo de camión refrigerado: -30 °C a +30 °C)
    df = df[(df['temp_celsius'] >= -30.0) & (df['temp_celsius'] <= 30.0)]
    print(f"Filas tras filtrar temperaturas anómalas: {len(df)}")

    # Regla 5: Dominio de Datos (Estados de envío válidos en la empresa)
    estados_validos = ['ENTREGADO', 'EN_TRANSITO', 'EN_REPARTO', 'PENDIENTE']
    df = df[df['estado_envio'].isin(estados_validos)]
    print(f"Filas tras validar catálogo de estados: {len(df)}\n")

    print("=== PASO 3: EXPORTACIÓN Y VERIFICACIÓN FINAL ===")
    # Exportar sin incluir el índice propio de Pandas
    df.to_csv(ruta_salida, index=False)
    
    filas_finales = len(df)
    hash_final = obtener_sha256(ruta_salida)

    print(f"Filas finales limpias: {filas_finales}")
    print(f"Total registros descartados: {filas_iniciales - filas_finales}")
    print(f"SHA-256 Limpio:   {hash_final}")
    print("===============================================")

if __name__ == "__main__":
    depurar_datos("datos/telemetria_envios.csv", "datos/telemetria_limpia.csv")