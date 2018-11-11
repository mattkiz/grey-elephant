#!/usr/bin/env bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install -r requirements.txt --user
sudo apt-get install -y chromium