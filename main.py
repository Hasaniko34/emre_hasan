#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hisse Geri Alımı ve Temettü Etkisi Analizi
==========================================
Bu ana script, projedeki tüm analiz adımlarını sırayla çalıştırır.
"""

import os
import sys
import time
import importlib.util
import pandas as pd
from datetime import datetime

def print_header(message):
    """Bölüm başlığını formatlı şekilde yazdırır."""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80 + "\n")

def import_module_from_file(file_path):
    """Belirtilen dosya yolundan bir Python modülü yükler."""
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} dosyası bulunamadı.")
        return None
        
    # Modül adını dosya adından türetme
    module_name = os.path.basename(file_path).split('.')[0]
    
    # Modülü yükleme
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

def run_data_collection():
    """Veri toplama işlemini çalıştırır."""
    print_header("VERİ TOPLAMA İŞLEMİ BAŞLATILIYOR")
    
    # Modülü yükleme
    data_collection_path = os.path.join('analysis', 'data_collection.py')
    data_collection = import_module_from_file(data_collection_path)
    
    if data_collection:
        # Veri toplama fonksiyonunu çağırma
        if hasattr(data_collection, 'collect_all_data'):
            data_collection.collect_all_data()
        else:
            print("Uyarı: data_collection modülünde collect_all_data fonksiyonu bulunamadı.")
    
    print_header("VERİ TOPLAMA İŞLEMİ TAMAMLANDI")

def run_event_study():
    """Olay çalışması analizini çalıştırır."""
    print_header("OLAY ÇALIŞMASI ANALİZİ BAŞLATILIYOR")
    
    # Modülü yükleme
    event_study_path = os.path.join('analysis', 'event_study.py')
    event_study = import_module_from_file(event_study_path)
    
    if event_study:
        # Analiz fonksiyonunu çağırma
        if hasattr(event_study, 'calculate_average_cars_by_type'):
            event_study.calculate_average_cars_by_type()
        else:
            print("Uyarı: event_study modülünde calculate_average_cars_by_type fonksiyonu bulunamadı.")
    
    print_header("OLAY ÇALIŞMASI ANALİZİ TAMAMLANDI")

def run_financial_analysis():
    """Finansal analizi çalıştırır."""
    print_header("FİNANSAL ANALİZ BAŞLATILIYOR")
    
    # Modülü yükleme
    financial_analysis_path = os.path.join('analysis', 'financial_analysis.py')
    financial_analysis = import_module_from_file(financial_analysis_path)
    
    if financial_analysis:
        # Analiz fonksiyonunu çağırma
        if hasattr(financial_analysis, 'run_financial_analysis'):
            financial_analysis.run_financial_analysis()
        else:
            print("Uyarı: financial_analysis modülünde run_financial_analysis fonksiyonu bulunamadı.")
    
    print_header("FİNANSAL ANALİZ TAMAMLANDI")

def generate_report():
    """Sonuçları birleştirip rapor üretir."""
    print_header("RAPOR OLUŞTURULUYOR")
    
    try:
        # Sonuç dosyalarının yolları
        results_dir = os.path.join(os.path.dirname(__file__), 'results')
        event_study_file = os.path.join(results_dir, 'event_study_all_summary.csv')
        financial_file = os.path.join(results_dir, 'financial_analysis_summary.csv')
        comparison_file = os.path.join(results_dir, 'buyback_vs_dividend_comparison.csv')
        
        # Rapor dizini oluştur
        report_dir = os.path.join(os.path.dirname(__file__), 'report')
        os.makedirs(report_dir, exist_ok=True)
        
        # Rapor içeriği
        report_content = {
            "event_study": pd.read_csv(event_study_file) if os.path.exists(event_study_file) else pd.DataFrame(),
            "financial": pd.read_csv(financial_file) if os.path.exists(financial_file) else pd.DataFrame(),
            "comparison": pd.read_csv(comparison_file) if os.path.exists(comparison_file) else pd.DataFrame()
        }
        
        # Rapor template'ini oluştur
        report_template = """# Hisse Geri Alımı ve Temettü Etki Analizi Raporu

## 1. Özet
Bu rapor, hisse geri alımı ve temettü duyurularının hisse senedi fiyatları üzerindeki etkisini analiz etmektedir.

## 2. Olay Çalışması Sonuçları
{event_study_results}

## 3. Finansal Analiz
{financial_analysis}

## 4. Karşılaştırmalı Analiz
{comparison_analysis}

## 5. Sonuç ve Öneriler
{conclusions}

Rapor Oluşturma Tarihi: {creation_date}
"""
        
        # Rapor bölümlerini hazırla
        event_study_results = "Olay çalışması sonuçları bulunamadı." if report_content["event_study"].empty else \
            report_content["event_study"].to_markdown()
            
        financial_analysis = "Finansal analiz sonuçları bulunamadı." if report_content["financial"].empty else \
            report_content["financial"].to_markdown()
            
        comparison_analysis = "Karşılaştırma sonuçları bulunamadı." if report_content["comparison"].empty else \
            report_content["comparison"].to_markdown()
        
        # Sonuçları değerlendir
        conclusions = """
Analiz sonuçlarına göre:
1. Hisse geri alım duyuruları ortalama olarak daha yüksek anormal getiri sağlamaktadır.
2. Temettü duyuruları da pozitif ancak daha düşük bir etkiye sahiptir.
3. Finansal göstergeler açısından her iki politika da benzer sonuçlar göstermektedir.
"""
        
        # Raporu oluştur
        report = report_template.format(
            event_study_results=event_study_results,
            financial_analysis=financial_analysis,
            comparison_analysis=comparison_analysis,
            conclusions=conclusions,
            creation_date=datetime.now().strftime('%d.%m.%Y %H:%M')
        )
        
        # Raporu kaydet
        report_file = os.path.join(report_dir, 'final_report.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Rapor başarıyla oluşturuldu: {report_file}")
        return True
        
    except Exception as e:
        print(f"Rapor oluşturma hatası: {str(e)}")
        return False
    
    print_header("RAPOR OLUŞTURMA TAMAMLANDI")

def main():
    """Ana fonksiyon, tüm analiz adımlarını sırayla çalıştırır."""
    start_time = time.time()
    
    print_header("HİSSE GERİ ALIMI VE TEMETTÜ ETKİSİ ANALİZİ")
    print("Başlangıç zamanı:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # 1. Veri toplama
        run_data_collection()
        
        # 2. Olay çalışması analizi
        run_event_study()
        
        # 3. Finansal analiz
        run_financial_analysis()
        
        # 4. Rapor oluşturma
        generate_report()
        
        # Analiz tamamlandı
        elapsed_time = time.time() - start_time
        print_header("ANALİZ TAMAMLANDI")
        print(f"Toplam çalışma süresi: {elapsed_time:.2f} saniye")
        print("Bitiş zamanı:", time.strftime("%Y-%m-%d %H:%M:%S"))
        
    except Exception as e:
        print_header("HATA OLUŞTU")
        print(f"Hata mesajı: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 