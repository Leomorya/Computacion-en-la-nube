FROM node:18

# Crear directorio /home/app
RUN mkdir -p /home/app

# Establecer directorio de trabajo /home/app
WORKDIR /home/app

# Copiar solo los archivos necesarios
COPY index.js package.json package-lock.json prueba.html /home/app/

# Instalar dependencias y ejecutar nodemon
RUN /bin/sh -c "npm install -g nodemon && npm install && npm install ejs"

# Exponer puerto 3000
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["nodemon", "index.js"] 