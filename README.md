# API Mesa de Ayuda

## Dependencias

1. Docker
Link de instalación: https://docs.docker.com/engine/install/ubuntu/

2. Python 3.8
3. virtualenv


## Ambiente
Solicitar archivo `.env` y cambiar las url según el proyecto.
Para el caso del BOT, por favor crear un BOT nuevo en telegram y asignar ese TOKEN al `.env`

OBS: el archivo `.env` debe ir en la carpeta API, es decir,
```
mesa-de-ayuda-api > API > .env
```

## Instalar dependencias

Entrar al ambiente de desarrollo
````
source env/bin/activate
```

Ejecutar 
```
pip3 install -r dev_requirements.txt
```

Obtener e instalar imagen de redis para docker
```
docker run -p 6379:6379 -d redis:5
```

## Configuración de BOT
En caso de estar en ambiente local, será necesario crear un tunnel con tu computador para recibir los mensajes
del bot.

Para esto, descargar NGROK y usarlo en el puerto 8000

Posteriormente ejcutar el CURL para setear el webhook de Telegram

```
curl --location --request POST 'https://api.telegram.org/bot<TOKEN>/setWebHook?url=https://<URL_NGROK>/webhooks/bot/'
```

A su vez, asignar la `API_URL=<URL_NGROK>` en el archivo `.env`

## Ejecución

Correr migraciones y runserver
```
python manage.py migrate
python manage.py runserver
```



