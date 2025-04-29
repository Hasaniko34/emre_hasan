#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veri Toplama İşlemleri
======================
Bu script, projede kullanılacak hisse senedi verilerini toplamak için kullanılır.
"""

import os
import csv
import json
import datetime as dt
import requests
from time import sleep

# Ana dizin yolunu belirleme
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Klasörleri oluştur
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Şirket listemiz (ticker sembolü, şirket adı, sektör, ülke)
COMPANIES = [
    # ABD Şirketleri
    ('AAPL', 'Apple Inc.', 'Teknoloji', 'ABD'),
    ('MSFT', 'Microsoft Corporation', 'Teknoloji', 'ABD'),
    ('JNJ', 'Johnson & Johnson', 'Sağlık', 'ABD'),
    ('KO', 'The Coca-Cola Company', 'Tüketici Ürünleri', 'ABD'),
    ('XOM', 'Exxon Mobil Corporation', 'Enerji', 'ABD'),
    
    # Türkiye Şirketleri
    ('THYAO.IS', 'Türk Hava Yolları', 'Ulaşım', 'Türkiye'),
    ('TUPRS.IS', 'Türkiye Petrol Rafinerileri A.Ş.', 'Enerji', 'Türkiye'),
    ('EREGL.IS', 'Ereğli Demir ve Çelik Fabrikaları T.A.Ş.', 'Metal', 'Türkiye'),
    ('AKBNK.IS', 'Akbank T.A.Ş.', 'Finans', 'Türkiye'),
    ('BIMAS.IS', 'BİM Birleşik Mağazalar A.Ş.', 'Perakende', 'Türkiye')
]

# Olay tarihleri (event dates)
# Format: (şirket ticker'ı, olay tarihi (YYYY-MM-DD), olay türü ('buyback' veya 'dividend'), açıklama)
EVENTS = [
    # Hisse Geri Alım Duyuruları
    ('AAPL', '2023-01-15', 'buyback', 'Apple 90 milyar dolarlık ek hisse geri alım programı duyurdu'),
    ('MSFT', '2022-09-20', 'buyback', 'Microsoft 60 milyar dolarlık hisse geri alım programı duyurdu'),
    ('THYAO.IS', '2022-03-15', 'buyback', 'THY 1 milyar TL\'lik hisse geri alım programı duyurdu'),
    ('EREGL.IS', '2021-11-10', 'buyback', 'Ereğli Demir Çelik 500 milyon TL\'lik hisse geri alım programı duyurdu'),
    ('XOM', '2022-04-26', 'buyback', 'Exxon Mobil 30 milyar dolarlık hisse geri alım programı duyurdu'),
    
    # Temettü Duyuruları
    ('JNJ', '2023-02-10', 'dividend', 'Johnson & Johnson 2023Q1 temettü duyurusu'),
    ('KO', '2022-10-18', 'dividend', 'Coca-Cola 2022Q4 temettü duyurusu'),
    ('TUPRS.IS', '2023-03-22', 'dividend', 'Tüpraş 2022 yılı temettü duyurusu'),
    ('AKBNK.IS', '2022-03-25', 'dividend', 'Akbank 2021 yılı temettü duyurusu'),
    ('BIMAS.IS', '2023-04-05', 'dividend', 'BİM 2022 yılı temettü duyurusu')
]

def ensure_directories():
    """Gerekli klasörlerin varlığını kontrol eder ve yoksa oluşturur."""
    directories = [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def fetch_stock_data_from_yahoo(ticker, start_date, end_date):
    """
    Yahoo Finance API kullanarak hisse senedi verilerini indirir.
    
    Parametreler:
    ticker (str): Hisse senedi sembolü
    start_date (str): Başlangıç tarihi (YYYY-MM-DD)
    end_date (str): Bitiş tarihi (YYYY-MM-DD)
    
    Dönüş:
    list: Günlük hisse fiyat verisi
    """
    # Yahoo Finance API endpoint
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    # String formatında tarihleri timestamp'e çevirme
    start_timestamp = int(dt.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(dt.datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    
    # API parametreleri
    params = {
        "period1": start_timestamp,
        "period2": end_timestamp,
        "interval": "1d",  # Günlük veri
        "events": "history",
        "includeAdjustedClose": True
    }
    
    # API isteği gönderme
    url = f"{base_url}{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        # Veri kontrolü
        if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
            result = data["chart"]["result"][0]
            
            timestamps = result["timestamp"]
            quotes = result["indicators"]["quote"][0]
            adjclose = result["indicators"]["adjclose"][0]["adjclose"] if "adjclose" in result["indicators"] else None
            
            # Veriyi CSV formatında hazırlama
            stock_data = []
            for i in range(len(timestamps)):
                date = dt.datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d')
                row = {
                    "Date": date,
                    "Open": quotes["open"][i] if quotes["open"][i] is not None else "NaN",
                    "High": quotes["high"][i] if quotes["high"][i] is not None else "NaN",
                    "Low": quotes["low"][i] if quotes["low"][i] is not None else "NaN",
                    "Close": quotes["close"][i] if quotes["close"][i] is not None else "NaN",
                    "Adj Close": adjclose[i] if adjclose and adjclose[i] is not None else "NaN",
                    "Volume": quotes["volume"][i] if quotes["volume"][i] is not None else "NaN"
                }
                stock_data.append(row)
            
            return stock_data
        else:
            print(f"Hata: {ticker} için veri alınamadı.")
            return []
            
    except Exception as e:
        print(f"Hata: {ticker} için veri alırken bir hata oluştu - {str(e)}")
        return []

def save_to_csv(data, filename):
    """Veriyi CSV dosyasına kaydeder."""
    if not data:
        print(f"Uyarı: {filename} için kaydedilecek veri yok.")
        return
    
    fieldnames = data[0].keys()
    filepath = os.path.join(RAW_DATA_DIR, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Veri {filepath} dosyasına kaydedildi.")

def collect_all_data():
    """Tüm şirketler için veri toplar."""
    ensure_directories()
    
    # Olaydan 1 yıl öncesi ve 1 yıl sonrası veri toplama
    for event in EVENTS:
        ticker, event_date, event_type, _ = event
        
        # Olay tarihinden 1 yıl önce ve 1 yıl sonra
        event_dt = dt.datetime.strptime(event_date, "%Y-%m-%d")
        start_date = (event_dt - dt.timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = (event_dt + dt.timedelta(days=365)).strftime("%Y-%m-%d")
        
        print(f"{ticker} için {event_type} olayı ({event_date}) verisi toplanıyor...")
        
        # Yahoo Finance'dan veri çekme
        stock_data = fetch_stock_data_from_yahoo(ticker, start_date, end_date)
        
        if stock_data:
            # Veriyi kaydetme
            filename = f"{ticker}_{event_type}_{event_date.replace('-', '')}.csv"
            save_to_csv(stock_data, filename)
        
        # API'ye fazla yük bindirmemek için bekleme
        sleep(1)
    
    # Piyasa endeksleri için de veri toplama
    for market_index in ['^GSPC', '^XU100.IS']:  # S&P 500 ve BIST 100
        print(f"{market_index} endeksi için veri toplanıyor...")
        
        # Tüm olayları kapsayacak tarih aralığı
        all_dates = [dt.datetime.strptime(event[1], "%Y-%m-%d") for event in EVENTS]
        min_date = min(all_dates) - dt.timedelta(days=400)  # Tahmin dönemi için biraz daha öncesi
        max_date = max(all_dates) + dt.timedelta(days=400)
        
        start_date = min_date.strftime("%Y-%m-%d")
        end_date = max_date.strftime("%Y-%m-%d")
        
        # Veri çekme ve kaydetme
        market_data = fetch_stock_data_from_yahoo(market_index, start_date, end_date)
        
        if market_data:
            filename = f"{market_index}_{start_date.replace('-', '')}_to_{end_date.replace('-', '')}.csv"
            save_to_csv(market_data, filename)
        
        sleep(1)
    
    # Şirket ve olay bilgilerini JSON olarak kaydetme
    save_company_info()
    save_event_info()
    
    print("Veri toplama tamamlandı.")

def save_company_info():
    """Şirket bilgilerini JSON dosyasına kaydeder."""
    companies_dict = [
        {
            "ticker": ticker,
            "name": name,
            "sector": sector,
            "country": country
        }
        for ticker, name, sector, country in COMPANIES
    ]
    
    filepath = os.path.join(DATA_DIR, "companies.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(companies_dict, f, ensure_ascii=False, indent=4)
    
    print(f"Şirket bilgileri {filepath} dosyasına kaydedildi.")

def save_event_info():
    """Olay bilgilerini JSON dosyasına kaydeder."""
    events_dict = [
        {
            "ticker": ticker,
            "date": date,
            "type": event_type,
            "description": description
        }
        for ticker, date, event_type, description in EVENTS
    ]
    
    filepath = os.path.join(DATA_DIR, "events.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(events_dict, f, ensure_ascii=False, indent=4)
    
    print(f"Olay bilgileri {filepath} dosyasına kaydedildi.")

if __name__ == "__main__":
    collect_all_data() 