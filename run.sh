#!/bin/bash

# Hisse Geri Alımı ve Temettü Etkisi Analizi
# Çalıştırma script'i

# Renkli çıktı için ANSI renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Başlık yazdırma fonksiyonu
print_header() {
    echo -e "\n${BOLD}${BLUE}==============================================${NC}"
    echo -e "${BOLD}${BLUE} $1 ${NC}"
    echo -e "${BOLD}${BLUE}==============================================${NC}\n"
}

# Ortam kontrol fonksiyonu
check_environment() {
    print_header "ORTAM KONTROLÜ YAPILIYOR"
    
    # Python kontrolü
    echo -e "${YELLOW}Python sürümü kontrol ediliyor...${NC}"
    if command -v python3 &>/dev/null; then
        PYTHON="python3"
        echo -e "${GREEN}Python bulundu:${NC} $(python3 --version)"
    elif command -v python &>/dev/null; then
        PYTHON="python"
        echo -e "${GREEN}Python bulundu:${NC} $(python --version)"
    else
        echo -e "${RED}HATA: Python yüklü değil!${NC}"
        exit 1
    fi
    
    # Gerekli dizinlerin kontrolü
    echo -e "\n${YELLOW}Proje dizinleri kontrol ediliyor...${NC}"
    
    # Dizinleri kontrol et, yoksa oluştur
    for DIR in "data" "data/stock" "data/market" "data/events" "data/financial" "results" "report"; do
        if [ ! -d "$DIR" ]; then
            echo -e "  ${DIR} dizini oluşturuluyor..."
            mkdir -p "$DIR"
        fi
    done
    
    echo -e "${GREEN}Tüm gerekli dizinler hazır!${NC}"
}

# Ana script
main() {
    print_header "HİSSE GERİ ALIMI VE TEMETTÜ ETKİSİ ANALİZİ"
    echo -e "Başlangıç zamanı: $(date "+%Y-%m-%d %H:%M:%S")"
    
    # Ortam kontrolü
    check_environment
    
    # Ana Python script'ini çalıştır
    print_header "ANALİZ BAŞLATILIYOR"
    echo -e "${YELLOW}main.py çalıştırılıyor...${NC}"
    
    if $PYTHON main.py; then
        print_header "ANALİZ BAŞARIYLA TAMAMLANDI"
        echo -e "${GREEN}İşlem başarılı bir şekilde tamamlandı.${NC}"
    else
        print_header "ANALİZ SIRASINDA HATA OLUŞTU"
        echo -e "${RED}İşlem sırasında bir hata oluştu. Lütfen hata mesajlarını kontrol edin.${NC}"
        exit 1
    fi
    
    echo -e "\n${BOLD}Bitiş zamanı: $(date "+%Y-%m-%d %H:%M:%S")${NC}"
}

# Script'i çalıştır
main 