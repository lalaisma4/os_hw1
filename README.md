# CPU Zamanlama Algoritmaları

Bu proje, farklı CPU zamanlama algoritmalarını simüle eder ve karşılaştırmalı analiz yapar.

## Kullanım

Programı çalıştırmak için:

```bash
python3 main.py <input_file.csv>
```

Örnek:
```bash
python3 main.py inp1.csv
python3 main.py inp2.csv
```

## Giriş Dosyası Formatı

CSV dosyası şu sütunları içermelidir:
- Process_ID: Süreç kimliği
- Arrival_Time: Varış zamanı
- CPU_Burst_Time: CPU kullanım süresi
- Priority: Öncelik (high, normal, low)

## Algoritmalar

1. **FCFS** (First Come First Served)
2. **Preemptive SJF** (Shortest Job First)
3. **Non-Preemptive SJF**
4. **Round Robin** (Quantum=4)
5. **Preemptive Priority**
6. **Non-Preemptive Priority**

## Çıktılar

Program her algoritma için ayrı bir dosya oluşturur. Dosyalar `results_<input_name>` klasöründe bulunur.

Her sonuç dosyası şunları içerir:
- Zaman tablosu
- Maksimum ve ortalama bekleme süresi
- Maksimum ve ortalama tamamlanma süresi
- Belirli zamanlarda throughput değerleri (T=50, 100, 150, 200)
- CPU verimliliği
- Bağlam değiştirme sayısı

## Parametreler

- Bağlam değiştirme süresi: 0.001 birim zaman
- Round Robin kuantum süresi: 4 birim zaman
- Öncelik değerleri: high=1, normal=2, low=3

## Gereksinimler

- Python 3.x
- Standart Python kütüphaneleri (csv, sys, os)
