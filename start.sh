#!/bin/sh

PYTHON_EXECUTABLE="python3.10"
VENV_DIR="venv"

if [[ ! -d $VENV_DIR ]]; then
	echo "No venv found, creating one"
	$PYTHON_EXECUTABLE -m venv $VENV_DIR

	echo "Installing dependencies via pip"
	source $VENV_DIR/bin/activate
	$PYTHON_EXECUTABLE -m pip install -r requirements.txt
fi

mkdir -p data/img_orig
mkdir -p data/res/image
mkdir -p data/res/thumb
mkdir -p data/res/avatar
cp -r src/js data/res/
cp -r src/css data/res/
cp -r src/img data/res/

source $VENV_DIR/bin/activate
$PYTHON_EXECUTABLE modules/main.py 

