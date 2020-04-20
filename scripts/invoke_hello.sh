sam build
sam local invoke "HelloWorldFunction" \
    -e events/discogs-wantlist.json \
    --parameter-overrides $(jq -r 'to_entries[] | "\(.key)=\(.value)"' .env/devel.json)