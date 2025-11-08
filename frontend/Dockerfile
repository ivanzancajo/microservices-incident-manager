# --- Etapa 1: Compilar la aplicación Vue.js ---
FROM node:20-alpine AS build

# Establece el directorio de trabajo
WORKDIR /app

# Declara el argumento que recibiremos de docker-compose
ARG VITE_API_URL

# Lo establece como variable de entorno para que 'npm run build' lo use
ENV VITE_API_URL=${VITE_API_URL}

# Copia package.json y package-lock.json primero (para cache de capas)
COPY package*.json ./

# Instala dependencias
RUN npm install

# Copia el resto del código fuente
COPY . .

# Ejecuta el build
RUN npm run build-only

# --- Etapa 2: Servir con Nginx ---
FROM nginx:stable-alpine

# Copia los archivos estáticos compilados desde la etapa 'build'
COPY --from=build /app/dist /usr/share/nginx/html

# Copia el archivo de configuración de Nginx que crearemos
# (Este archivo define el reverse proxy)
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Nginx escucha en el puerto 80 por defecto
EXPOSE 80