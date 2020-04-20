sam build
sam local start-api \
    --parameter-overrides $(jq -r 'to_entries[] | "\(.key)=\(.value)"' .env/prod.json)