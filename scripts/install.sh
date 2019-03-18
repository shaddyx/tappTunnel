#!/bin/sh

cd ..
rm -rf venv
virtualenv venv --python=python3.6
cd venv/bin
. activate 
cd ../../src
pip install -r requirements.txt