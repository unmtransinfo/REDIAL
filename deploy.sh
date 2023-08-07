#!/bin/bash

#!/bin/bash

LETSENCRYPT_EMAIL="pkedia@salud.unm.edu"
DNSNAME="unmtid-services.net"

docker run -it --rm --name certbot \
    -v "$PWD/letsencrypt:/etc/letsencrypt" \
    -v "$PWD/lib/letsencrypt:/var/lib/letsencrypt" \
    certbot/certbot \
    certonly \
    -m $LETSENCRYPT_EMAIL \
    --manual \
    --preferred-challenges dns-01 \
    --no-eff-email \
    --manual-public-ip-logging-ok \
    --keep-until-expiring \
    --agree-tos \
    -d $DNSNAME \
    --server https://acme-v02.api.letsencrypt.org/directory

until curl --silent http://app:5555/health; do
    echo "App not yet healthy. Waiting ...";
    sleep 1s;
done

curl -v http://app:5555/health
echo "App healthy. Starting nginx...";

# bash docker-entrypoint.sh nginx -g "daemon off;"

docker-compose -f docker-compose-prod.yml --env-file .env.prod up --build -d