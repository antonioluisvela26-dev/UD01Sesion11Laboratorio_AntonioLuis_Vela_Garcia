#!/bin/bash

echo "=== 1. Creando estructura de directorios en HDFS ==="
hdfs dfs -mkdir -p /empresa/logistica/input

echo "=== 2. Subiendo el archivo saneado a HDFS ==="
hdfs dfs -put /workspace/telemetria_limpia.csv /empresa/logistica/input/

echo "=== 3. Listando el directorio distribuido ==="
hdfs dfs -ls /empresa/logistica/input/

echo "=== 4. Mostrando las primeras líneas almacenadas en HDFS ==="
hdfs dfs -head /empresa/logistica/input/telemetria_limpia.csv

echo "=== 5. Auditando bloques físicos y nodos con FSCK ==="
hdfs fsck /empresa/logistica/input/telemetria_limpia.csv -files -blocks -locations