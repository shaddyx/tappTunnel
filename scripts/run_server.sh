#!/bin/bash

pushd ../venv/bin/
. ./activate
popd

pushd ../src
python serverMain.py $@
popd
