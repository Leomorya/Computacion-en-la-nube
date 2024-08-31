#!/bin/bash

# Inicializa LXD si no está ya configurado
echo "inicilizando lxd"
lxd init --auto

# pasa el file yaml al home
echo "pasando el archivo yaml al home"
mv /vagrant/config.yaml /home/vagrant/


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
echo "pasando el archivo a /var/www/html ..."
lxc file push items/index.html my-web-container/var/www/html/index.html


