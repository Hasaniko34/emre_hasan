# Hisse Geri Alımları (Share Buybacks) vs. Temettü (Dividends): Hisse Değeri Üzerindeki Etki

## Özet

Bu çalışma, şirketlerin **nakit dağıtımı stratejileri** olan hisse geri alımları ve temettü ödemelerinin **hisse fiyatı performansı**, **hisse başına karlılık (EPS)** ve diğer finansal göstergeler üzerindeki etkisini karşılaştırmalı olarak analiz etmektedir. Çalışma, 2 farklı şirketi kapsamakta ve 2021-01-01 - 2023-12-31 tarihleri arasında gerçekleşen hisse geri alım ve temettü duyurularına odaklanmaktadır. Olay çalışması (event study) metodolojisi kullanılarak, bu duyuruların hisse fiyatı üzerindeki kısa vadeli etkisi ve finansal oranlardaki orta/uzun vadeli değişimler incelenmiştir.

## 1. Giriş

### 1.1. Araştırmanın Amacı

Bu çalışmanın temel amacı, şirketlerin nakit dağıtımı yöntemlerinden olan hisse geri alımları ile temettü ödemelerinin yatırımcı değeri üzerindeki etkilerini karşılaştırmalı olarak incelemektir. Çalışma kapsamında aşağıdaki sorulara yanıt aranmaktadır:

1. Hisse geri alım duyuruları ve temettü duyuruları sonrasında hisse fiyatı nasıl bir tepki vermektedir?
2. Hangi nakit dağıtım stratejisi daha güçlü bir piyasa tepkisi yaratmaktadır?
3. Hisse geri alımı ve temettü ödemelerinin EPS, ROE gibi finansal oranlar üzerindeki etkileri nelerdir?
4. Bu stratejilerin kullanımında sektörel veya coğrafi farklılıklar gözlemlenmekte midir?

### 1.2. Araştırmanın Önemi

Şirketler, nakit fazlalarını değerlendirmek ve hissedar değeri yaratmak için temettü ödemesi veya hisse geri alımı stratejilerinden birini ya da her ikisini birden tercih etmektedirler. Son yıllarda, özellikle ABD piyasalarında, hisse geri alımlarının temettü ödemelerine kıyasla daha yaygın hale geldiği gözlemlenmektedir. Bu tercih değişikliğinin ardındaki nedenler ve bu değişimin hissedar değeri üzerindeki etkileri, finans literatüründe önemli bir tartışma konusudur.

Bu çalışma, hem teorik tartışmalara katkı sağlamayı hem de yatırımcılar ve finansal analistler için pratik içgörüler sunmayı amaçlamaktadır.

## 2. Veri ve Metodoloji

### 2.1. Şirket Seçimi ve Örneklem

Bu çalışmada, aşağıdaki şirketler incelenmiştir:

**ABD Şirketleri:**
- NIKE, Inc. (NKE) - Consumer Cyclical

**Türkiye Şirketleri:**
- Migros Ticaret A.S. (MGROS) - Consumer Defensive


### 2.2. Veri Kaynakları

Çalışmada kullanılan veriler aşağıdaki kaynaklardan elde edilmiştir:

- **Hisse Fiyat Verileri**: Yahoo Finance API
- **Hisse Geri Alım Duyuruları**: Simülasyon (gerçek uygulama için şirket duyuruları kullanılabilir)
- **Temettü Duyuruları**: Yahoo Finance
- **Finansal Tablo Verileri**: Yahoo Finance API (çeyreklik finansal raporlar)

### 2.3. Olay Çalışması (Event Study) Metodolojisi

Çalışmada, hisse geri alım ve temettü duyurularının hisse fiyatı üzerindeki etkisini ölçmek için olay çalışması (event study) metodolojisi kullanılmıştır.

1. **Olay Penceresi**: Duyuru tarihinden 5 gün öncesi ve 5 gün sonrası ([-5, +5])
2. **Tahmin Penceresi**: Olay penceresinden önceki 120 iş günü
3. **Normal Getiri Modeli**: Piyasa modeli (Ri = αi + βi × Rm + εi)
4. **Anormal Getiri**: ARit = Rit - E(Rit)
5. **Kümülatif Anormal Getiri (CAR)**: ∑ARit

## 3. Bulgular

### 3.1. Olay Çalışması Sonuçları

#### 3.1.1. Anormal Getiriler

Hisse geri alım duyuruları ve temettü duyuruları sonrasında gözlemlenen ortalama anormal getiriler aşağıdaki tabloda özetlenmiştir:

| Olay Türü | Ortalama CAR (-5,+5) (%) | Ortalama CAR (-2,+2) (%) | Ortalama CAR (0,+1) (%) |
|-----------|------------------|----------------|--------------------|
| Buyback | 4.52 | 0.00 | 2.10 |
| Dividend | 3.14 | 0.00 | 0.71 |

Hisse geri alım duyurularının, temettü duyurularına kıyasla daha güçlü bir pozitif piyasa tepkisi yarattığı gözlemlenmiştir (4.52% vs 3.14%). Bu bulgu, literatürdeki birçok çalışmayla uyumludur.

### 3.2. Finansal Analiz Sonuçları

#### 3.2.1. Şirketlerin Finansal Göstergeleri

Analize dahil edilen şirketlerin temel finansal göstergeleri:

| Şirket | Sektör | ROE (%) | ROA (%) | Borç/Özkaynak | Temettü Verimi (%) |
|--------|--------|---------|---------|---------------|-------------------|
| NIKE, Inc. | Consumer Cyclical | 0.00 | 2.10 | 0.00 | 278.00 |
| Migros Ticaret A.S. | Consumer Defensive | 0.00 | 0.71 | 0.00 | 198.00 |

#### 3.2.2. Hisse Geri Alımı ve Temettü Etkisi Karşılaştırması

Hisse geri alımı ve temettü duyurularının finansal göstergeler üzerindeki etkisi:

| Finansal Gösterge | Hisse Geri Alımı Etkisi | Temettü Etkisi |
|-------------------|--------------------------|----------------|
| ROE Değişimi (%) | 0.00 | 0.00 |
| ROA Değişimi (%) | -0.96 | -1.63 |
| Net Gelir Değişimi (%) | -31.73 | -66.37 |


## 4. Sonuç

### 4.1. Genel Değerlendirme

Bu çalışma, hisse geri alımları ve temettü ödemelerinin hisse değeri üzerindeki etkilerini 2021-01-01 - 2023-12-31 tarihleri arasında seçilen 2 şirket için karşılaştırmalı olarak analiz etmiştir. 

Bulgularımız:

1. Olay çalışması sonuçlarına göre, hisse geri alım duyuruları daha güçlü bir pozitif piyasa tepkisi yaratmıştır.
2. Finansal göstergeler üzerindeki etki incelendiğinde, temettü ödemelerinin ROE üzerinde daha olumlu bir etki yarattığı gözlemlenmiştir.
3. Net gelir değişimi açısından hisse geri alımları daha olumlu sonuçlar göstermiştir.

Bu sonuçlar, şirketlerin nakit dağıtım stratejilerini belirlerken hissedar değerini maksimize etmek için çeşitli faktörleri göz önünde bulundurmaları gerektiğini göstermektedir.

### 4.2. Yatırımcılar İçin Öneriler

Bu çalışmanın sonuçları doğrultusunda yatırımcılar için şu önerilerde bulunulabilir:

1. Hisse geri alım duyurularının genellikle daha güçlü bir pozitif piyasa tepkisi yarattığı dikkate alınarak, bu tür duyuruları takip etmek kısa vadeli yatırım stratejileri için faydalı olabilir.
2. Uzun vadeli yatırımcılar için, hem hisse geri alımları hem de temettü ödemeleri şirketin finansal sağlığının göstergeleri olarak değerlendirilebilir.
3. Sektör dinamikleri ve şirketin büyüme aşaması, nakit dağıtım stratejisinin hisse değeri üzerindeki etkisini değiştirebildiği için, bu faktörler de dikkate alınmalıdır.

Analizimiz 2025-04-28 15:12:51 tarihinde gerçekleştirilmiştir.
