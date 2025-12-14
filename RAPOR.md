# CPU Zamanlama Algoritmaları Proje Raporu

## 1. Giriş

Bu projede 6 farklı CPU zamanlama algoritması gerçekleştirilmiş ve iki farklı veri seti üzerinde test edilmiştir. Her algoritmanın performans metrikleri karşılaştırılmıştır.

## 2. Uygulanan Algoritmalar

1. **FCFS (First Come First Served)**: Süreçler varış sırasına göre işlenir
2. **Preemptive SJF**: En kısa işi seçer, kesmeye izin verir
3. **Non-Preemptive SJF**: En kısa işi seçer, kesme olmaz
4. **Round Robin**: Her süreç sırayla 4 birimlik kuantum alır
5. **Preemptive Priority**: Önceliğe göre, kesmeye izin verir
6. **Non-Preemptive Priority**: Önceliğe göre, kesme olmaz

## 3. Performans Metrikleri

### 3.1 Inp1 Sonuçları

| Algoritma | Ort. Bekleme | Ort. Tamamlanma | CPU Verimlilik | Bağlam Değiştirme |
|-----------|--------------|-----------------|----------------|-------------------|
| FCFS | 813.50 | 824.00 | 99.94% | 199 |
| Preemptive SJF | 537.00 | 547.50 | 99.94% | 212 |
| Non-Preemptive SJF | 537.42 | 547.92 | 99.94% | 199 |
| Round Robin | 1091.70 | 1102.20 | 99.92% | 599 |
| Preemptive Priority | 833.63 | 844.13 | 99.94% | 201 |
| Non-Preemptive Priority | 824.77 | 835.27 | 99.94% | 199 |

### 3.2 Throughput Karşılaştırması (Inp1)

T=50 için:
- Preemptive SJF: 11 işlem (en yüksek)
- FCFS: 9 işlem

T=200 için:
- Preemptive SJF: 42 işlem (en yüksek)
- FCFS: 19 işlem

## 4. Analiz

### 4.1 En İyi Performans

**Preemptive SJF** ve **Non-Preemptive SJF** algoritmaları:
- En düşük ortalama bekleme süresi (~537)
- En düşük ortalama tamamlanma süresi (~547)
- En yüksek throughput değerleri

### 4.2 En Kötü Performans

**Round Robin** algoritması:
- En yüksek ortalama bekleme süresi (1091.70)
- En yüksek ortalama tamamlanma süresi (1102.20)
- En fazla bağlam değiştirme (599)
- CPU verimliliği diğerlerinden biraz düşük (99.92%)

### 4.3 FCFS ve Priority Algoritmaları

- Orta seviye performans gösterirler
- Bağlam değiştirme sayıları düşük
- CPU verimliliği yüksek

## 5. Sonuçlar

1. **SJF algoritmaları** kısa işleri önceliklendirdiği için en iyi sonuçları vermiştir
2. **Round Robin** adil olmakla birlikte çok fazla bağlam değiştirmeye neden olur
3. **FCFS** basit ama optimal değildir
4. **Priority** algoritmaları önceliğe göre iyi sonuç verir ama starvation riski vardır
5. Tüm algoritmalar %99+ CPU verimliliği sağlamıştır

## 6. Teknik Detaylar

- Bağlam değiştirme süresi: 0.001 birim
- Round Robin kuantum: 4 birim
- Öncelik değerleri: high=1, normal=2, low=3
- Test veri seti: 200 süreç
- Programlama dili: Python 3
