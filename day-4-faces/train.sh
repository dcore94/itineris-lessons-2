#!/bin/bash

face_service_url=$1
image_url=$2
label=$3
embeddings_folder_url=$4

echo "Downloading image from workspace"
./download-from-ws.sh $image_url picture

echo "Calling face service for processing"
curl -X POST $face_service_url/process -F "image=@picture" -o embeddings.json

echo "Running python script for annotating image and labelling embeddings"
python3 train.py $label

echo "Uploading embeddings to workspace"
./upload-to-ws.sh $embeddings_folder_url "$label"_embeddings.json

echo "copying results to ccp_data"
cp picture "$label".jpg embeddings.json "$label"_embeddings.json /ccp_data