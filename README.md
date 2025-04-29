# Hisse Geri Alımları vs. Temettü: Hisse Değeri Üzerindeki Etki

## Proje Tanımı
Bu proje, şirketlerin **nakit dağıtımı** stratejilerinden temettü ödemesi ile hisse geri alımlarının **hisse fiyatı**, **hisse başına kârlılık (EPS)** ve **piyasa tepkisi** üzerindeki etkisini analiz etmektedir. Projede olay çalışması (event study) yöntemi kullanılarak, hisse geri alım açıklaması ve temettü ödemesi açıklaması sonrasında hisse fiyatlarındaki anormal getiriler (abnormal returns) incelenmektedir.

## Araştırma Soruları
- Hisse geri alım açıklaması (veya uygulaması) sonrasında hisse fiyatı nasıl bir tepki veriyor?
- Temettü ödemelerinin düzenliliği ve miktarı hisse değerini hangi yönde etkiliyor?
- Şirket kârlılığı (ROE, ROA, EPS) değişiyor mu?
- Olay çalışması (event study) yaparak, yatırımcıların duyuru tarihine yakın abnormal getirilerinde (CAR, AAR) bir fark oluyor mu?

## Proje Yapısı
```
buyback_dividend_project/
├── data/                     # Ham ve işlenmiş veri dosyaları
├── analysis/                 # Analiz kodları
├── results/                  # Analiz sonuçları ve grafikler
└── report/                   # Sonuç raporu
```

## Veri Kaynakları
- Yahoo Finance API (yfinance) - Hisse fiyat ve hacim verileri
- KAP (Kamuyu Aydınlatma Platformu) - Türk şirketleri için duyurular
- EDGAR (SEC) - Uluslararası şirketler için duyurular
- Şirketlerin finansal tabloları

## Metodoloji
1. Olay Çalışması (Event Study)
   - Anormal Getiri (AR) ve Kümülatif Anormal Getiri (CAR) hesaplama
   - Olay penceresi analizi
2. Oran Analizi
   - EPS, ROE, ROA değişimlerinin incelenmesi
3. Karşılaştırmalı Analiz
   - Temettü vs. Hisse Geri Alımı politikalarının karşılaştırılması

## Kullanılan Şirketler
10 farklı şirket, çeşitli sektörlerden seçilmiştir:
1. [Şirket 1] - [Sektör]
2. [Şirket 2] - [Sektör]
...
10. [Şirket 10] - [Sektör] 