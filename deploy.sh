# !bin/bash

npm run build

aws s3 cp sandbox/static/oscar/css/styles.css s3://bedswing-bucket/static/oscar/css/styles.css --profile personal

set -e

git add .

#git commit -m 'deploy'

echo "yes" | python sandbox/manage.py collectstatic

echo "starting deployment"

eb deploy bedswing-app

echo "deployed"