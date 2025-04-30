#!/usr/bin/env bash
# exit on error
set -o errexit

# Gerekli dizinleri oluştur
mkdir -p results
mkdir -p report
mkdir -p data

# Python paketlerini kur
pip install -r requirements.txt

# Statik dosyaları topla (gerekiyorsa)
# python manage.py collectstatic --no-input 