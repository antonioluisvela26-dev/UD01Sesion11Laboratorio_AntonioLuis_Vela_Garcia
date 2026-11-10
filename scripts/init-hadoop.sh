#!/bin/bash

# 1. Configurar HDFS (Master URI y Réplicas)
echo '<configuration><property><name>fs.defaultFS</name><value>hdfs://hadoop-lab:9000</value></property></configuration>' > /opt/hadoop/etc/hadoop/core-site.xml
echo '<configuration><property><name>dfs.replication</name><value>1</value></property></configuration>' > /opt/hadoop/etc/hadoop/hdfs-site.xml

# 2. Crear el wrapper de 'jps' en el directorio de binarios de Hadoop (con permisos)
cat << 'EOF' > /opt/hadoop/bin/jps
#!/bin/bash
ps -ef | grep java | grep -v grep | awk '{print $2, $NF}' | sed 's/.*\./ /'
echo "$$ Jps"
EOF
chmod +x /opt/hadoop/bin/jps

# 3. Formatear NameNode solo si es la primera ejecución
if [ ! -d /tmp/hadoop-hadoop/dfs/name/current ]; then
  hdfs namenode -format -nonInteractive -force
fi

# 4. Arrancar los 4 demonios obligatorios
hdfs --daemon start namenode
hdfs --daemon start datanode
yarn --daemon start resourcemanager
yarn --daemon start nodemanager

# 5. Mantener el contenedor en ejecución
tail -f /dev/null