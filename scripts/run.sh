#!/bin/bash

pushd ../venv/bin/
. ./activate
popd

pushd ../src
python clientMain.py $@
popd
