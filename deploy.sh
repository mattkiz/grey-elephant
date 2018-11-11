#!/usr/bin/env bash
apt-get -y install chromium
gunicorn -b :$PORT main:app