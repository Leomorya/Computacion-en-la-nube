#!/bin/bash
echo "descargando y instalando consul"
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install consul -y


echo "creando el agente de consul"
#consul agent -server -ui -bootstrap-expect=1 -data-dir=. -node=server1 -bind=192.168.100.12 -#client=0.0.0.0 & 

sudo cat ./Shared_Folder_proyect01/agent_haproxy.txt > /etc/consul.d/consul.hcl

echo "habilitar el servicio consul"
sudo systemctl restart consul

echo "actualizando el servidor haproxy"
sudo apt update && apt upgrade -y

echo "instalando  haproxy"
sudo apt install haproxy -y

echo "configurando el archivo  haproxy en /etc/haproxy/haproxy.cfg"
sudo cat ./Shared_Folder_proyect01/haproxi_config >> /etc/haproxy/haproxy.cfg

echo "configurando el archivo la salida del error 503.http"
sudo cat ./Shared_Folder_proyect01/503.txt > /etc/haproxy/errors/503.http

echo "corriendo haproxy "
sudo systemctl restart haproxy
