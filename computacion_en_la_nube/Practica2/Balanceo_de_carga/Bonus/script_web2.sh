#!/bin/bash
echo "actualizando web2"
sudo apt update && apt upgrade -y

echo "instalando  apache2 en web2"
sudo apt install apache2 -y

echo "copiando la pagina web en /var/www/html/index.html "
sudo cp ./paginas_web/indexweb2.html /var/www/html/index.html

echo "corriendo apache2 "
sudo systemctl enable apache2
