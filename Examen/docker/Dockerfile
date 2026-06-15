FROM debian:latest

RUN apt-get update && apt-get install -y \
    nginx \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/nebez/floppybird /var/www/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
