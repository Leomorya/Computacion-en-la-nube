#!/bin/bash
echo "actualizando haproxy"
sudo apt update && apt upgrade -y

echo "instalando  haproxy"
sudo apt install haproxy -y

echo "corriendo haproxy "
sudo systemctl enable haproxy

echo "configurando el archivo  haproxy en /etc/haproxy/haproxy.cfg"
sudo cat ./paginas_web/conf_haproxy >> /etc/haproxy/haproxy.cfg

echo "corriendo haproxy "
sudo systemctl restart haproxy
