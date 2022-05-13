#!/bin/sh
# Note: Call it from dev parent folder ../dev
# as dev/start.sh

# change to dev path
cd dev/

#   TELEGRAM TOKEN
telegram_token="1914846977:AAGW_BXn_ia8zECT5laArhrgIZEFXk3Yb1M"

#   INICIAR NGROK y OBTENER LINK
gnome-terminal -- ./ngrok http 8000 # puedes usar otra terminal

sleep 5

curl http://127.0.0.1:4040/api/tunnels > tunnels.json

ngrok_link=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')


#   REEMPLAZAR LINK
sed -i "s,^API_URL=.*$,API_URL='$ngrok_link'," ../API/.env

sed -i "s,^API_URL='https://,API_URL='," ../API/.env


#   ESTABLECER EL WEBHOOK
curl --location --request POST "https://api.telegram.org/bot$telegram_token/setWebHook?url=$ngrok_link/webhooks/bot/"

#   RUN REDIS
docker run -p 6379:6379 -d redis:5

## back to parent folder
cd ..

# # RUN CELERY
# cd mesa-de-ayuda-api
# gnome-terminal -- celery -A API worker -E

# # RUN FLOWER
# #celery -A API flower --address=127.0.0.6 --port=5566
# gnome-terminal -- celery -A API flower --address=127.0.0.6 --port=5566

# # RUN CELERY BEAT
# #celery -A API beat -S celerybeatmongo.schedulers.MongoScheduler -l info
# gnome-terminal -- celery -A API beat -S celerybeatmongo.schedulers.MongoScheduler -l info