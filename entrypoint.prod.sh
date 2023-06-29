#!/bin/bash

# echo "teshgtaeskljhgfsdklj"
cp $HOME/.aws/credentials /root/.aws/credentials 
gunicorn --reload --timeout 90 --bind 0.0.0.0:8000 app:app