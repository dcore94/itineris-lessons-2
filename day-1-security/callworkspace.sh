#!/bin/bash
IAM="https://accounts.d4science.org/auth/realms/d4science/protocol/openid-connect/token"
CTX="/d4science.research-infrastructures.eu/FARM/ITINERIS_Training-Platform"

WS="https://api.d4science.org/workspace"
QUERY="/items/8d8bc783-2f04-4a46-9fa3-d881d01e5755/download"
URL=$WS/$QUERY

echo -n "Enter password: "
read -s password

AT=$(curl -X POST $IAM -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=password" -d "client_id=itineris.d4science.org" \
    -d "username=your_username" -d "password=$password" \
    -d "scope=d4s-context:$CTX" | jq -r '.access_token')

curl $URL -H "Authorization: Bearer $AT" --output file.png