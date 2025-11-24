FROM nginx:alpine

# Eliminamos la configuración por defecto de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiamos nuestra configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Exponemos el puerto 80 (interno del contenedor)
EXPOSE 80