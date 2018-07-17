#!/bin/bash


source virt/bin/activate

### Upload CSS to bucket
npm run build
python sandbox/manage.py collectstatic
gsutil cp  sandbox/public/static/staticfiles.json gs://bedswing-bucket/static/staticfiles.json
gsutil rsync -R  sandbox/public/static/oscar/css gs://bedswing-bucket/static/oscar/css

##Icon to Bucket
gsutil rsync -R  sandbox/public/static/images gs://bedswing-bucket/static/images

## Dockerize 
pip freeze > requirements.txt
docker build -t gcr.io/brave-standard-180615/bedswing .
gcloud docker -- push gcr.io/brave-standard-180615/bedswing:latest


##Restar

kubectl delete --all pods
