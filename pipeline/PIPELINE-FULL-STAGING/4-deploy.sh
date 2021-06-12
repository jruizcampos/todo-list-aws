#!/bin/bash

source py37-venv/bin/activate
yes|sam deploy --config-env staging // el parametro con valor staging lo debe leer del archivo .toml
