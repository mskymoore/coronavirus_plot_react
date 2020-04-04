#!/bin/bash

pip3 install virtualenv

echo "export PATH=$PATH:/home/admin/.local/bin" >> ~/.bashrc

source ~/.bashrc

virtualenv env

source env/bin/activate

pip install -r src/requirements.txt