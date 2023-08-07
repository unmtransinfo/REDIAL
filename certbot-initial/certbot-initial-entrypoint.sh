certbot certonly \
        --standalone \
        -d $DOMAIN_NAME \
        -m $EMAIL_ADDRESS \
        --rsa-key-size "2048" \
        --agree-tos \
        -n \
        --server https://acme-staging-v02.api.letsencrypt.org/directory \
        --staging
        # --force-renewal
        # -vvv