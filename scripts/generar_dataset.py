import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

hubs = ['HUB-MADRID', 'HUB-BARCELONA', 'HUB-VALENCIA', 'HUB-SEVILLA', 'HUB-BILBAO']
estados = ['ENTREGADO', 'EN_TRANSITO', 'EN_REPARTO', 'PENDIENTE']

registros = []
base_time = datetime(2026, 3, 1, 8, 0, 0)

for i in range(1, 290):
    envio_id = f"ENV-2026-{i:04d}"
    vehiculo = f"FLOTA-{random.randint(100, 999)}"
    timestamp = base_time + timedelta(minutes=i*15)
    origen = random.choice(hubs)
    destino = random.choice([h for h in hubs if h != origen])
    peso = round(random.uniform(5.0, 500.0), 2)
    temp = round(random.uniform(-5.0, 8.0), 1)
    lat = round(40.4167 + random.uniform(-2.0, 2.0), 4)
    lon = round(-3.7037 + random.uniform(-2.0, 2.0), 4)
    estado = random.choice(estados)
    
    registros.append([envio_id, vehiculo, timestamp.isoformat(), origen, destino, peso, temp, lat, lon, estado])

df = pd.DataFrame(registros, columns=[
    'id_envio', 'id_vehiculo', 'timestamp_lectura', 'origen', 
    'destino', 'peso_kg', 'temp_celsius', 'latitud', 'longitud', 'estado_envio'
])

# Introducción deliberada de anomalías (10 filas)
anomalias = [
    ['ENV-2026-0005', 'FLOTA-105', '2026-03-01T09:00:00', 'HUB-MADRID', 'HUB-BARCELONA', 45.2, 3.1, 40.4, -3.7, 'ENTREGADO'], # Duplicado
    ['ENV-2026-0291', 'FLOTA-404', '2026-03-02T10:00:00', 'HUB-SEVILLA', None, 120.0, 4.0, 37.3, -5.9, 'EN_TRANSITO'], # Nulo en destino
    ['ENV-2026-0292', 'FLOTA-505', '2026-03-02T10:15:00', 'HUB-VALENCIA', 'HUB-BILBAO', None, 2.5, 39.4, -0.3, 'EN_REPARTO'], # Nulo en peso
    ['ENV-2026-0293', 'FLOTA-606', '2026-03-02T10:30:00', 'HUB-BILBAO', 'HUB-MADRID', 80.0, None, 43.2, -2.9, 'EN_TRANSITO'], # Nulo en temp
    ['ENV-2026-0294', 'FLOTA-707', '2026-03-02T10:45:00', 'HUB-MADRID', 'HUB-SEVILLA', -45.50, 5.0, 40.4, -3.7, 'EN_TRANSITO'], # Peso negativo
    ['ENV-2026-0295', 'FLOTA-808', '2026-03-02T11:00:00', 'HUB-BARCELONA', 'HUB-VALENCIA', 210.0, 98.4, 41.3, 2.1, 'EN_TRANSITO'], # Temp extrema
    ['ENV-2026-0296', 'FLOTA-909', '2026-03-02T11:15:00', 'HUB-SEVILLA', 'HUB-MADRID', 150.0, 4.2, 37.3, -5.9, 'DESCONOCIDO_ERROR'], # Estado no catalogado
    ['ENV-2026-0010', 'FLOTA-110', '2026-03-01T10:15:00', 'HUB-MADRID', 'HUB-VALENCIA', 60.0, 2.1, 40.4, -3.7, 'ENTREGADO'], # Duplicado
    ['ENV-2026-0297', 'FLOTA-301', '2026-03-02T11:30:00', 'HUB-VALENCIA', 'HUB-BARCELONA', 95.0, 3.8, 39.4, -0.3, 'ENTREGADO'],
    ['ENV-2026-0298', 'FLOTA-302', '2026-03-02T11:45:00', 'HUB-BILBAO', 'HUB-SEVILLA', 310.0, -1.2, 43.2, -2.9, 'EN_REPARTO']
]

df_anomalias = pd.DataFrame(anomalias, columns=df.columns)
df_final = pd.concat([df, df_anomalias], ignore_index=True)
df_final.to_csv('datos/telemetria_envios.csv', index=False)