#!/bin/bash

source py37-venv/bin/activate
set -x
sam validate --template template.yaml
sam build --use-container
