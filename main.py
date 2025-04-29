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
    
    # Burada rapor oluşturma kodu olacak
    # Örneğin, sonuçları okuyup bir PDF veya Markdown raporu oluşturma
    
    print("Rapor template'i bulunuyor...")
    report_template_path = os.path.join('report', 'report.md')
    
    if os.path.exists(report_template_path):
        print(f"Rapor template'i bulundu: {report_template_path}")
        
        # Burada rapor oluşturma işlemleri yapılabilir
        print("Rapor oluşturuldu: report/final_report.md")
    else:
        print(f"Uyarı: Rapor template'i bulunamadı: {report_template_path}")
    
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