# CLAUDE.md — CodeEnhancer Comparative Study
> Bu dosya, Claude Code'un proje bağlamını anlaması için hazırlanmıştır.
> Her oturumda önce bu dosyayı oku. Değişiklik yaptıktan sonra TODO.md ve DECISIONS.md'yi güncelle.

---

## Projenin Amacı

Bu proje, CENG 467 (Natural Language Understanding and Generation) dersi için hazırlanan bir dönem projesidir.

**Temel soru:** Farklı LLM'ler ve farklı prompting stratejileri kombinasyonları, LLM-üretimi Python kodundaki güvenlik açıklarını ne ölçüde azaltabiliyor?

Baseline olarak alınan **CodeEnhancer** (JAIST Cybersecurity Research Lab) framework'ü, GPT-4o + SAST araçları (Bandit, Pylint) + iteratif geri bildirim döngüsü kullanan bir Stage 1 + Stage 2 mimarisine sahiptir. Bu projede yalnızca **Stage 1** genişletilecek; Stage 2 (fine-tuning) kapsam dışıdır.

---

## Kapsam (Hoca Direktifine Göre)

- ✅ Stage 1: Farklı LLM'ler ile deney
- ✅ Stage 1: Farklı prompt stratejileri ile deney
- ✅ Performans karşılaştırması (Bandit zafiyet oranı, iterasyon sayısı, metrikler)
- ❌ Stage 2 (fine-tuning) — kapsam dışı
- ❌ Donanım optimizasyonu (AWQ, quantization) — kapsam dışı

---

## Deney Matrisi (Kesinleşti — 2026-05-11)

|                          | Zero-shot | Few-shot | Chain-of-Thought |
|--------------------------|-----------|----------|------------------|
| Gemini 1.5 Flash         | planlı    | planlı   | planlı           |
| Gemini 2.0 Flash         | planlı    | planlı   | planlı           |
| Llama 3.1 8B (Ollama)    | planlı    | planlı   | planlı           |

> Gemini modelleri ücretsiz Google Generative AI API. Llama 3.1 8B Ollama ile local çalışır (M4 + 16GB). OpenAI kapsam dışı. Bkz. DECISIONS.md #005.

---

## Proje Yapısı

```
CodeEnhancer/                  ← fork'lanan orijinal repo
├── code_generator.py          ← LLM'e prompt gönderir, kod üretir
├── code_validator.py          ← Pylint + Bandit + LLM judge döngüsü
├── dataset.json               ← Giriş promptları (LLMSecEval formatı)
├── baseline/
│   ├── code/                  ← Üretilen .py dosyaları
│   ├── *_dialogue.json        ← Konuşma logları
│   ├── results.json           ← Özet sonuçlar
│   └── all_dialogues.json     ← Tüm iterasyonların logları
│
├── experiments/               ← Her deney kombinasyonu için klasör (3 model × 3 strateji = 9)
│   ├── gemini15flash_zeroshot/
│   ├── gemini15flash_fewshot/
│   ├── gemini15flash_cot/
│   ├── gemini20flash_zeroshot/
│   ├── gemini20flash_fewshot/
│   ├── gemini20flash_cot/
│   ├── llama31_8b_zeroshot/
│   ├── llama31_8b_fewshot/
│   └── llama31_8b_cot/
│
├── prompts/                   ← [YENİ] Prompt şablonları
│   ├── zero_shot.py
│   ├── few_shot.py
│   └── chain_of_thought.py
│
├── analysis/                  ← [YENİ] Sonuç analiz scriptleri
│   ├── compare_results.py
│   └── visualize.py
│
├── data/                      ← [YENİ] Veri setleri
│   └── llmseceval/
│
├── CLAUDE.md                  ← Bu dosya
├── TODO.md                    ← Görev listesi (her değişiklikte güncelle)
├── DECISIONS.md               ← Kararlar ve gerekçeler (her değişiklikte güncelle)
└── requirements.txt           ← Bağımlılıklar
```

---

## Veri Seti

**LLMSecEval** kullanılacak.
- 150 doğal dil promptu
- MITRE CWE Top 25 güvenlik açıklarını hedefliyor
- Her prompt için beklenen çıktı: güvenlik açığı içermeyen Python kodu

Mid-phase için 15-20 prompt yeterli. Finale kadar tüm 150 prompt.

---

## Metrikler

Her deney kombinasyonu için şunlar raporlanacak:
- **İlk üretimde zafiyet oranı** (Bandit hit @ iteration 0)
- **Final zafiyet oranı** (5 iterasyon sonunda kalan)
- **Ortalama düzeltme iterasyonu** (kaçıncı turda temizlendi)
- **Düzeltilemeyen zafiyet oranı** (5 iterasyon sonunda hâlâ açık)
- **CWE bazında kırılım** (hangi zafiyet tipi hangi modelde dirençli)

---

## Kurallar (Claude Code İçin)

1. Yaptığın her kod değişikliğinden sonra **TODO.md**'yi güncelle.
2. Bir karar aldığında veya bir seçenek reddedildiğinde **DECISIONS.md**'ye yaz.
3. Yeni bir dosya oluştururken proje yapısını yukarıdaki şemaya göre yerleştir.
4. `experiments/` klasörü altında her kombinasyon izole olmalı — birbirinin çıktısını kirletmemeli.
5. Asla `dataset.json`'ı doğrudan düzenleme; veri setini `data/` klasörü altında yönet.
6. Her script'in başında hangi deney kombinasyonu için çalıştığını belirten bir yorum satırı olsun.
7. API anahtarları asla kod içinde sabit (hardcoded) olmamalı — `.env` dosyasından oku.

---

## Önemli Bağlantılar

- Orijinal repo: https://github.com/cyb3rlab/CodeEnhancer
- Fork: [Kendi fork URL'ni buraya ekle]
- LLMSecEval veri seti: https://github.com/tuhh-softsec/LLMSecEval
- Mid-phase teslim tarihi: 3 gün sonra
- Final teslim tarihi: ~1.5 ay sonra
