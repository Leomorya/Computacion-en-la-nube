#!/bin/bash


echo "descargando y instalando consul"
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install consul -y


echo "creando el agente de consul"
#consul agent -server -ui -bootstrap-expect=1 -data-dir=. -node=server1 -bind=192.168.100.12 -#client=0.0.0.0 & 

sudo cat ./Shared_Folder_proyect01/agent_service1.txt > /etc/consul.d/consul.hcl

echo "habilitar el servicio consul"
sudo systemctl restart consul

echo "instalando nodejs y npm"
sudo apt install nodejs -y && sudo apt install npm -y

echo "copiando el micro servicio"
cp -r ./Shared_Folder_proyect01/consulService1 /home/vagrant/

echo "llendo a la carpeta del servicio y instalando consul y express con npm"
cd consulService1/app && npm install consul express



echo "ejecutando el servicio en dos replicas"

nohup node index.js 3000 &
#nohup node index.js 5000 &
nohup node index.js 3001 &
#nohup node index.js 3002 &

#sudo systemctl enable consul
