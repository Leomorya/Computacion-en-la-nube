#!/bin/bash

# Inicializa LXD si no está ya configurado
echo "inicilizando lxd"
lxd init --auto

# creando un archivo yaml
echo "creando el archivo yaml"
cat > config.yaml <<EOF
instances:
  - name: my-web-container
    image: ubuntu:22.04
EOF

# Crea el contenedor utilizando el archivo YAML
echo "creando el contenedor lxc"
lxc launch ubuntu:22.04 my-web-container < config.yaml

# forwarding de puertos
echo "# forwarding de puertos ..."
lxc config device add my-web-container http proxy listen=tcp:0.0.0.0:80 connect=tcp:127.0.0.1:80

#Instalando Apache2
echo "Instalando Apache2..."
lxc exec my-web-container -- /bin/bash -c "apt update && apt upgrade -y && apt install apache2 -y"
echo "Apache2 instalado correctamente."

# creando el sitio web
echo "creando el archivo html del sitio web..."
lxc exec my-web-container -- /bin/bash -c "cd /var/www/html && echo \"<!DOCTYPE html><html><head><title>Mi Sitio Web</title></head><body><h1>Bienvenido a mi sitio web!</h1></body></html>\" > index.html"


