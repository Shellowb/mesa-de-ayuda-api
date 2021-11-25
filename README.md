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
```
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

### NGROK
para descargar ngrok (tunel) ir a la página de descargas de ngrok [enlace](https://ngrok.com/download)

En general los pasos son:

```sh
unzip /path/to/ngrok.zip
./ngrok authtoken <your_auth_token>
./ngrok http <port> 
# Solo necesitas este último una vez que ya lo hayas configurado
# En general port es el que usas para correr django, por default 8000
```

> Para poder usar el tunel es necesario registrarse y crear una cuenta una vez hecho eso. tendrás acceso a un dashboard.
ahí ve a la sección. Getting Started>Setup & Installation>
En la sección 3.Connect yout account: esta el comando para configurar tu token.
En linux al menos el token se guarda en `/home/<user>/.ngrok2/ngrok.yml`

### Telegram
Si no has creado un bot de desarrollo puedes hacerlo iniciando un chat con el BotFather
```sh
/start
/newbot
name_bot # Si tiene que terminar en bot, pero puede no llevar _
```
Al finalizar este proceso se te entregará un TOKEN. este token es tu llave para configurar al bot.

Posteriormente, para setear el webhook de Telegram, ejcutar el CURL:
```
curl --location --request POST 'https://api.telegram.org/bot<TOKEN>/setWebHook?url=https://<URL_NGROK>/webhooks/bot/'
```
>Recuerda haber iniciado el tunel con `./ngrok http <port>`

A su vez, asignar la `API_URL=<URL_NGROK>` en el archivo `.env` sin https://

## Ejecución
> recuerda que para cada vez que corras ngrok, debes cambiar la API_URL del .env y además setear el webhook a telegram.

Con el fin de evitar hacer todos los cambios manualmente cada vez que se te apague el computador, te recomiendo correr el siguiente escript que iniciará el tunel y además hará los remplazos y seteos automáticamente. Así solo tienes que correr el proyecto de django y ya esta.
```sh
#!/bin/sh


#   TELEGRAM TOKEN
telegram_token="<token>"


#   INICIAR NGROK y OBTENER LINK
gnome-terminal -- <ngrok path>/ngrok http 8000 # puedes usar otra terminal

sleep 5

curl http://127.0.0.1:4040/api/tunnels > tunnels.json

ngrok_link=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')


#   REEMPLAZAR LINK
sed -i "s,^API_URL=.*$,API_URL='$ngrok_link'," mesa-de-ayuda-api/API/.env

sed -i "s,^API_URL='https://,API_URL='," mesa-de-ayuda-api/API/.env


#   ESTABLECER EL WEBHOOK
curl --location --request POST "https://api.telegram.org/bot$telegram_token/setWebHook?url=$ngrok_link/webhooks/bot/"
```

### Ayuda nunca corrí un Script
para correr estos commandos necesitas tener instalados `curl`, `jq` y `sed`.

En Ubuntu los puedes instalar como
```
sudo apt install curl jq sed
```
En Arch
```
sudo pacman -Syu curl jq sed
```

crea un archivo que se llame `start.sh` en la carpeta que contenga el proyecto.

Cambia los permisos de ejecución con:
```sh
chmod a+x ./start.sh
```
y luego puedes ejecutar el script cada vez reinicies o apagues el pc con:
```
./start.sh
```


### Python
Correr migraciones y runserver
```
python manage.py migrate
python manage.py runserver
```



