#!/bin/bash
IAM="https://accounts.d4science.org/auth/realms/d4science/protocol/openid-connect/token"
CTX="/d4science.research-infrastructures.eu/FARM/ITINERIS_Training-Platform"

CATALOGUE="https://api.d4science.org/catalogue"
QUERY="items?limit=10&offset=0"
URL=$CATALOGUE/$QUERY

echo -n "Enter password: "
read -s password

AT=$(curl -X POST $IAM -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=password" -d "client_id=itineris.d4science.org" \
    -d "username=your_username" -d "password=$password" \
    -d "scope=d4s-context:$CTX" | jq -r '.access_token')

curl $URL -H "Authorization: Bearer $AT"