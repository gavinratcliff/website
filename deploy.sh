#!/bin/bash

mkdir -p generated
python3 generate_website.py
rm -r /var/www/html/*
cp -r generated/* /var/www/html/
