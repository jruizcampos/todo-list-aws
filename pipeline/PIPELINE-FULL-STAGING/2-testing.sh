#!/bin/bash

source py37-venv/bin/activate
set -x
flake8 src
if [[ $? -ne 0 ]]
then
	exit 1
fi

radon cc src
if [[ $? -ne 0 ]]
then
	exit 1
fi

bandit -r src
if [[ $? -ne 0 ]]
then
	exit 1
fi

cd test/unified/
coverage run TestToDoClass.py
coverage report -m
