#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Olay Çalışması (Event Study) Analizi
====================================
Bu script, hisse geri alımı ve temettü duyurularını takip eden hisse senedi fiyat 
hareketlerini analiz etmek için kullanılır. Olay etrafındaki anormal getiriler (AR) 
ve kümülatif anormal getiriler (CAR) hesaplanarak piyasa tepkisi ölçülür.
"""

import os
import json
import csv
import datetime as dt
import math
import statistics
from collections import defaultdict
import glob

# Ana dizin yolları
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')

# Sonuçlar klasörünü oluşturma
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Piyasa endeksleri
MARKET_INDICES = {
    'ABD': '^GSPC',    # S&P 500 
    'Türkiye': '^XU100.IS'  # BIST 100
}

def read_stock_data(file_path):
    """CSV dosyasından hisse senedi fiyat verilerini okur."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Sayısal değerleri float tipine çevirme
            for key in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
                try:
                    row[key] = float(row[key]) if row[key] != 'NaN' else None
                except (ValueError, KeyError):
                    row[key] = None
            data.append(row)
    return data

def read_market_data(market_index, start_date, end_date):
    """Piyasa endeksi verilerini okur."""
    # Eğer piyasa verileri daha önce indirilmişse, doğrudan oku
    market_files = glob.glob(os.path.join(RAW_DATA_DIR, f"{market_index}_*.csv"))
    
    if market_files:
        # En son indirilen dosyayı kullan
        market_file = sorted(market_files)[-1]
        market_data = read_stock_data(market_file)
        
        # Tarihe göre filtrele
        filtered_data = []
        for row in market_data:
            if start_date <= row['Date'] <= end_date:
                filtered_data.append(row)
        
        return filtered_data
    else:
        print(f"Uyarı: {market_index} için piyasa verisi bulunamadı.")
        return []

def calculate_returns(data):
    """Günlük getirileri hesaplar."""
    returns = []
    for i in range(1, len(data)):
        prev_close = data[i-1]['Close']
        curr_close = data[i]['Close']
        
        if prev_close is not None and curr_close is not None and prev_close > 0:
            daily_return = (curr_close / prev_close) - 1
        else:
            daily_return = None
            
        returns.append({
            'Date': data[i]['Date'],
            'Return': daily_return
        })
    
    return returns

def estimate_market_model(stock_returns, market_returns, estimation_window=120):
    """
    Piyasa modeli parametrelerini tahmin eder.
    
    Ri = alpha + beta * Rm + epsilon
    
    Ri: Hisse getirisi
    Rm: Piyasa getirisi
    alpha, beta: Model parametreleri
    epsilon: Hata terimi
    """
    # Hisse ve piyasa getirilerini eşleştirme
    paired_returns = []
    market_return_dict = {r['Date']: r['Return'] for r in market_returns}
    
    for stock_return in stock_returns[:estimation_window]:
        date = stock_return['Date']
        if date in market_return_dict and stock_return['Return'] is not None and market_return_dict[date] is not None:
            paired_returns.append((stock_return['Return'], market_return_dict[date]))
    
    if len(paired_returns) < 30:  # Yeterli veri yoksa
        print("Uyarı: Piyasa modeli tahmini için yeterli veri yok. Varsayılan değerler kullanılacak.")
        return 0, 1  # Varsayılan alpha=0, beta=1
    
    # Ortalamalar
    stock_mean = sum(r[0] for r in paired_returns) / len(paired_returns)
    market_mean = sum(r[1] for r in paired_returns) / len(paired_returns)
    
    # Kovaryans ve varyans
    numerator = sum((r[0] - stock_mean) * (r[1] - market_mean) for r in paired_returns)
    denominator = sum((r[1] - market_mean) ** 2 for r in paired_returns)
    
    if denominator == 0:
        beta = 1  # Varsayılan beta
    else:
        beta = numerator / denominator
    
    alpha = stock_mean - beta * market_mean
    
    return alpha, beta

def calculate_abnormal_returns(stock_returns, market_returns, event_date, alpha, beta, 
                               event_window=(-10, 10)):
    """
    Anormal getirileri (AR) ve kümülatif anormal getirileri (CAR) hesaplar.
    
    AR = Ri - (alpha + beta * Rm)
    CAR = sum(AR) for days in event window
    """
    market_return_dict = {r['Date']: r['Return'] for r in market_returns}
    
    # Olay tarihini bulma
    event_index = None
    for i, r in enumerate(stock_returns):
        if r['Date'] == event_date:
            event_index = i
            break
    
    if event_index is None:
        print(f"Uyarı: {event_date} tarihi bulunamadı.")
        return [], 0
    
    # Olay penceresi içindeki günler
    start_index = max(0, event_index + event_window[0])
    end_index = min(len(stock_returns) - 1, event_index + event_window[1])
    
    # Anormal getiriler
    abnormal_returns = []
    for i in range(start_index, end_index + 1):
        date = stock_returns[i]['Date']
        stock_return = stock_returns[i]['Return']
        market_return = market_return_dict.get(date)
        
        if stock_return is not None and market_return is not None:
            # Beklenen getiri
            expected_return = alpha + beta * market_return
            # Anormal getiri
            ar = stock_return - expected_return
            
            abnormal_returns.append({
                'Date': date,
                'Day': i - event_index,  # Olay gününe göreli gün
                'Stock Return': stock_return,
                'Market Return': market_return,
                'Expected Return': expected_return,
                'Abnormal Return': ar
            })
    
    # Kümülatif anormal getiri (CAR)
    car = sum(ar['Abnormal Return'] for ar in abnormal_returns)
    
    return abnormal_returns, car

def analyze_event(event, company_country):
    """Belirli bir olay için event study analizi yapar."""
    ticker, event_date, event_type, _ = event
    
    # İlgili hisse senedi veri dosyasını bulma
    file_pattern = f"{ticker}_{event_type}_{event_date.replace('-', '')}.csv"
    stock_files = glob.glob(os.path.join(RAW_DATA_DIR, file_pattern))
    
    if not stock_files:
        print(f"Uyarı: {ticker} için {event_date} tarihli veri bulunamadı.")
        return None
    
    stock_file = stock_files[0]
    stock_data = read_stock_data(stock_file)
    
    if not stock_data:
        print(f"Uyarı: {ticker} için veri okunamadı.")
        return None
    
    # Tarih aralığını belirleme
    start_date = stock_data[0]['Date']
    end_date = stock_data[-1]['Date']
    
    # Piyasa endeksini belirleme
    market_index = MARKET_INDICES.get(company_country, '^GSPC')  # Varsayılan olarak S&P 500
    
    # Piyasa verilerini okuma
    market_data = read_market_data(market_index, start_date, end_date)
    
    if not market_data:
        print(f"Uyarı: {market_index} için piyasa verisi bulunamadı.")
        return None
    
    # Günlük getirileri hesaplama
    stock_returns = calculate_returns(stock_data)
    market_returns = calculate_returns(market_data)
    
    # Piyasa modeli parametrelerini tahmin etme (olay öncesi dönem)
    alpha, beta = estimate_market_model(stock_returns, market_returns)
    
    # Anormal getirileri hesaplama
    abnormal_returns, car = calculate_abnormal_returns(stock_returns, market_returns, event_date, alpha, beta)
    
    if not abnormal_returns:
        print(f"Uyarı: {ticker} için anormal getiriler hesaplanamadı.")
        return None
    
    # Sonuçları yapılandırma
    result = {
        'ticker': ticker,
        'event_date': event_date,
        'event_type': event_type,
        'alpha': alpha,
        'beta': beta,
        'car': car,
        'abnormal_returns': abnormal_returns
    }
    
    return result

def save_event_study_results(results, output_file):
    """Event study analiz sonuçlarını CSV dosyasına kaydeder."""
    if not results:
        print("Uyarı: Kaydedilecek sonuç yok.")
        return
    
    # Tüm şirketler için özet tablo
    summary_data = []
    for result in results:
        summary_row = {
            'Ticker': result['ticker'],
            'Event Date': result['event_date'],
            'Event Type': result['event_type'],
            'Alpha': result['alpha'],
            'Beta': result['beta'],
            'CAR': result['car']
        }
        summary_data.append(summary_row)
    
    # Özet tabloyu kaydetme
    summary_file = os.path.join(RESULTS_DIR, f"{output_file}_summary.csv")
    with open(summary_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Ticker', 'Event Date', 'Event Type', 'Alpha', 'Beta', 'CAR']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_data)
    
    print(f"Özet sonuçlar {summary_file} dosyasına kaydedildi.")
    
    # Her şirket için detaylı AR tablolarını kaydetme
    for result in results:
        detail_file = os.path.join(RESULTS_DIR, f"{output_file}_{result['ticker']}_{result['event_date'].replace('-', '')}.csv")
        
        with open(detail_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Date', 'Day', 'Stock Return', 'Market Return', 'Expected Return', 'Abnormal Return']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result['abnormal_returns'])
        
        print(f"Detaylı sonuçlar {detail_file} dosyasına kaydedildi.")

def calculate_average_cars_by_type():
    """Olay türüne göre ortalama CAR değerlerini hesaplar."""
    # Şirket bilgilerini yükleme
    company_file = os.path.join(DATA_DIR, "companies.json")
    with open(company_file, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    # Şirket-ülke eşleştirmesini hazırlama
    company_countries = {company['ticker']: company['country'] for company in companies}
    
    # Olay bilgilerini yükleme
    event_file = os.path.join(DATA_DIR, "events.json")
    with open(event_file, 'r', encoding='utf-8') as f:
        events = json.load(f)
    
    # Her olay için event study analizi yapma
    all_results = []
    for event in events:
        ticker = event['ticker']
        event_date = event['date']
        event_type = event['type']
        description = event['description']
        
        company_country = company_countries.get(ticker, 'ABD')  # Varsayılan olarak ABD
        
        print(f"{ticker} için {event_date} tarihli {event_type} olayı analiz ediliyor...")
        result = analyze_event((ticker, event_date, event_type, description), company_country)
        
        if result:
            all_results.append(result)
    
    # Sonuçları kaydetme
    save_event_study_results(all_results, "event_study_all")
    
    # Olay türüne göre ortalama CAR değerlerini hesaplama
    cars_by_type = defaultdict(list)
    for result in all_results:
        cars_by_type[result['event_type']].append(result['car'])
    
    avg_cars = {}
    for event_type, cars in cars_by_type.items():
        avg_cars[event_type] = {
            'count': len(cars),
            'average': sum(cars) / len(cars) if cars else 0,
            'median': statistics.median(cars) if cars else 0,
            'std_dev': statistics.stdev(cars) if len(cars) > 1 else 0
        }
    
    # Ortalama CAR değerlerini kaydetme
    avg_file = os.path.join(RESULTS_DIR, "average_cars_by_type.csv")
    with open(avg_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Event Type', 'Count', 'Average CAR', 'Median CAR', 'Std Dev']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for event_type, stats in avg_cars.items():
            writer.writerow({
                'Event Type': event_type,
                'Count': stats['count'],
                'Average CAR': stats['average'],
                'Median CAR': stats['median'],
                'Std Dev': stats['std_dev']
            })
    
    print(f"Olay türüne göre ortalama CAR değerleri {avg_file} dosyasına kaydedildi.")
    
    return all_results, avg_cars

if __name__ == "__main__":
    calculate_average_cars_by_type() 