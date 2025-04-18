#!/bin/bash

face_service_url=$1
image_url=$2
embeddings_folder_url=$3

if [ -z "$4" ]; then
    threshold="0.7"
else
    threshold=$4
fi

echo "Downloading image from workspace"
./download-from-ws.sh $image_url picture

echo "Downloading embeddings folder"
./download-from-ws.sh $embeddings_folder_url embeddings.zip
unzip -jd target_embeddings embeddings.zip

echo "Calling face service for processing"
curl -X POST $face_service_url/process -F "image=@picture" -o embeddings.json

echo "Running python script for annotating image and comparing embeddings"
python3 predict.py $face_service_url/compare $threshold

echo "copying results to ccp_data"
cp picture output.jpg embeddings.json /ccp_data