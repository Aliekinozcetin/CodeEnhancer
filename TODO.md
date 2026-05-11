# TODO.md — CodeEnhancer Comparative Study
> Son güncelleme: 2026-05-11
> Claude Code: Bu dosyayı yaptığın her değişiklikten sonra güncelle. Tamamlananları ✅, devam edenleri 🔄, bloke olanları 🔴 ile işaretle.

---

## 🚨 ACİL — Mid-Phase Report (3 gün içinde)

- [ ] GitHub fork URL'sini CLAUDE.md'ye ekle
- [ ] Repo'yu local'de çalıştır (Python env kur, bağımlılıkları yükle)
- ✅ `.env` dosyası oluşturuldu (şablon hazır — gerçek API key'leri sen gireceksin)
- [ ] `.env` dosyasına gerçek OPENAI_API_KEY ve GOOGLE_API_KEY değerlerini gir
- ✅ `data/llmseceval/` klasörü oluşturuldu, LLMSecEval veri seti indirildi (150 prompt, 18 CWE)
- ✅ 3 model × 3 strateji = 9 deney, 135 kod dosyası üretildi
- ✅ `code_validator.py` Ollama'ya uyarlandı, test edildi (Bandit + Pylint + LLM döngüsü)
- [ ] Tüm deneylerin validasyonunu çalıştır (`python3 code_validator.py`)
- [ ] İki modelin sonuçlarını karşılaştıran basit bir tablo oluştur
- [ ] Mid-phase report taslağını yaz (bölüm 1, 2, 3, 4, 5)
- [ ] GitHub'a en az 3-4 anlamlı commit at (commit geçmişi hoca tarafından izleniyor)

---

## 📁 Altyapı & Kurulum

- ✅ `experiments/` klasör yapısı oluşturuldu (9 kombinasyon: 3 model × 3 strateji — tümü Gemini)
- ✅ `prompts/` klasörü oluşturuldu
  - ✅ `zero_shot.py` — orijinal CodeEnhancer system prompt'u
  - ✅ `few_shot.py` — 3 örnekli few-shot (CWE-78, CWE-89, CWE-502)
  - ✅ `chain_of_thought.py` — CoT formatında prompt
- ✅ `analysis/` klasörü oluşturuldu (henüz script yok)
  - ✅ `compare_results.py` — Bandit hit rate, çözüm oranı, CWE kırılımı, model/strateji karşılaştırması
  - ✅ `visualize.py` — 5 grafik: bandit hit rate, resolution rate, avg iterations, CWE heatmap, final status
- ✅ `requirements.txt` oluşturuldu (openai, google-generativeai, python-dotenv, matplotlib, pandas, bandit, pylint)
- ✅ `.gitignore` oluşturuldu (.env dahil)
- ✅ `code_generator.py` hardcoded API key → `.env`'den okuyacak şekilde düzeltildi
- ✅ `code_validator.py` hardcoded API key → `.env`'den okuyacak şekilde düzeltildi
- [ ] `README.md`'yi fork'a göre güncelle (proje amacını ve nasıl çalıştırılacağını açıkla)

---

## 🧪 Deneyler

### Prompt Stratejileri
- ✅ Zero-shot prompt şablonu yazıldı (`prompts/zero_shot.py`)
- ✅ Few-shot prompt şablonu yazıldı (`prompts/few_shot.py`, 3 örnek)
- ✅ Chain-of-Thought prompt şablonu yazıldı (`prompts/chain_of_thought.py`)
- ✅ Prompt şablonları `code_generator.py`'ye parametre olarak geçilebilir hale getirildi

### Model Entegrasyonları
- ✅ Llama 3.1 8B entegrasyonu (Ollama)
- ✅ DeepSeek-Coder 6.7B entegrasyonu eklendi (indiriliyor)
- ✅ Mistral 7B entegrasyonu eklendi (indiriliyor)
- ✅ Gemini kapsam dışı bırakıldı (rate limit sorunu)
- ✅ Tüm modeller Ollama üzerinden çalışıyor, tek client

### Deney Çalıştırma
- ✅ 15 prompt seçildi → `data/mid_phase_prompts.json` (12 CWE kategorisi, katmanlı örnekleme, seed=42)
- [ ] 150 prompt → final için
- [ ] Her kombinasyon: `experiments/<model>_<prompt_stratejisi>/` altına kaydet
- [ ] Her çalıştırmada random seed sabitle (tekrarlanabilirlik)

---

## 📊 Analiz & Değerlendirme

- [ ] Zafiyet oranı hesaplama scripti yaz
- [ ] CWE bazında kırılım tablosu oluştur
- [ ] Ortalama iterasyon sayısı hesapla
- [ ] Karşılaştırma tablosu (model × prompt stratejisi matrisi)
- [ ] En az 5 başarısız örnek seç → nitel hata analizi yaz

---

## 📝 Rapor (Final)

- [ ] LNCS LaTeX şablonunu indir
- [ ] Bölüm 1: Introduction
- [ ] Bölüm 2: Related Work (CodeEnhancer + prompting literature)
- [ ] Bölüm 3: Methodology
- [ ] Bölüm 4: Experimental Setup
- [ ] Bölüm 5: Results
- [ ] Bölüm 6: Error Analysis
- [ ] Bölüm 7: Discussion
- [ ] Bölüm 8: Conclusion
- [ ] Tablolar ve figürler ekle
- [ ] Atıflar ekle

---

## ✅ Tamamlananlar

_(Burası başlangıçta boş — Claude Code tamamladıkça buraya taşıyacak)_

---

## 🔴 Bloke / Karar Bekleniyor

_(Şu an bloke eden karar yok — tüm açık kararlar kesinleşti)_
