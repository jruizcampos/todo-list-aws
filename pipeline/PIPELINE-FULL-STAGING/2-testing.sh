#!/bin/bash

source py37-venv/bin/activate
set -x

#a) Prueba de Revisión estática de Código con radon
radon cc src -a -nc
echo 'Resultado:\n'.$?

#if [[ $? -ne 0 ]]
#then
#	exit 1
#fi

#b) Prueba de Calidad de Código con flake8
flake8 src
if [[ $? -ne 0 ]]
then
	exit 1
fi

#c) Prueba de Seguridad en el Código con bandit
bandit -r src
if [[ $? -ne 0 ]]
then
	exit 1
fi

cd tests/unit/
#coverage run TestToDoTableClass.py
#coverage report -m
