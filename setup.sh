name=ding_bot
docker stop ${name}
docker rm ${name}

docker run -id \
--name ${name} \
-v ./config/:/app/config/ \
buyfakett/ding_bot:latest