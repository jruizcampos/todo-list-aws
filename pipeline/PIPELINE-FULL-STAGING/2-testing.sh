#!/bin/bash

source py37-venv/bin/activate
set -x

# a) Prueba de Revisión estática de Código con radon
radon cc src -a -nc
# echo 'Resultado: '.$?

if [[ $? -ne 0 ]]
then
	echo '-Falló el test de revisión estática de código con radon'
	exit 1
else 
	echo echo '-El test de Revisión estática de código con radon terminó correctamente'
fi

# b) Prueba de Calidad de Código con flake8
flake8 src
if [[ $? -ne 0 ]]
then
	echo '-Falló el test de Calidad de código con flake8'
	exit 1
else 
	echo echo '-El test de Calidad de código con flake8 terminó correctamente'
fi

# c) Prueba de Seguridad en el Código con bandit
bandit -r src
if [[ $? -ne 0 ]]
then
	echo '-Falló el test de Seguridad en el código con bandit'
	exit 1
else 
	echo echo '-El test de Seguridad en el código con bandit terminó correctamente'
fi

cd tests/unit/
#coverage run TestToDoTableClass.py
#coverage report -m
