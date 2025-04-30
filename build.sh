#!/usr/bin/env bash
# exit on error
set -o errexit

# Python sürümünü belirt
export PYTHON_VERSION=3.11.4

# Gerekli dizinleri oluştur
mkdir -p results
mkdir -p report
mkdir -p data

# Pip önbelleğini temizle
pip cache purge || true

# Güncel pip'i kur
pip install --upgrade pip

# Python paketlerini kur
pip install --no-cache-dir -r requirements.txt

# Statik dosyaları topla (gerekiyorsa)
# python manage.py collectstatic --no-input 