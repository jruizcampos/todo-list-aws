#!/bin/bash

source py37-venv/bin/activate
set -x

#a) Prueba de Revisión estática de Código con radon
radon cc src -a -nc
echo 'Resultado: '.$?

if [[ $? -ne 0 ]]
then
	echo '-Falló el test de revisión estática de código con Radon'
	exit 1
fi

#b) Prueba de Calidad de Código con flake8
flake8 src
if [[ $? -ne 0 ]]
then
	echo '-Falló el test de Calidad de código con Flake8'
	exit 1
fi

#c) Prueba de Seguridad en el Código con bandit
#bandit -r src
#if [[ $? -ne 0 ]]
#then
#	exit 1
#fi

cd tests/unit/
#coverage run TestToDoTableClass.py
#coverage report -m
