#!/bin/bash
echo "actualizando haproxy"
sudo apt update && apt upgrade -y

echo "instalando  haproxy"
sudo apt install haproxy -y

echo "configurando el archivo  haproxy en /etc/haproxy/haproxy.cfg"
sudo cat ./Shared_Folder_proyect01/haproxi_config >> /etc/haproxy/haproxy.cfg

echo "configurando el archivo la salida del error 503.http"
sudo cat ./Shared_Folder_proyect01/503.txt > /etc/haproxy/errors/503.http

echo "corriendo haproxy "
sudo systemctl restart haproxy
