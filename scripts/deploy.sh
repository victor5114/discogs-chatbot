BUILD_PATH=./.aws-sam/build
TEMPLATE_PATH="${BUILD_PATH}/template.yaml"
PACKAGE_PATH="${BUILD_PATH}/packaged.yaml"

sam build && sam package --template-file $TEMPLATE_PATH \
    --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-1898s98r8g2g1 \
    --output-template-file $PACKAGE_PATH

sam deploy --template-file $PACKAGE_PATH \
    --stack-name "discogs-chatbot" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides $(jq -r 'to_entries[] | "\(.key)=\(.value)"' .env/prod.json)
