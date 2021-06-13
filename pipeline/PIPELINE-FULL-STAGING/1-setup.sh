#!/bin/bash
docker run -d --name dynamodb -p 8000:8000 amazon/dynamodb-local
sleep 10
aws dynamodb create-table --table-name localTable --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
pwd
cd src/
python3.7 -m venv py37-venv
source py37-venv/bin/activate
pip install -r requirements.txt
