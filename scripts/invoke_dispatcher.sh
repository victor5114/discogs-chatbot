sam build
sam local invoke "DisaptcherFunction" \
    -e events/discogs-bot-dispatcher.json \
    --parameter-overrides $(jq -r 'to_entries[] | "\(.key)=\(.value)"' .env/devel.json)