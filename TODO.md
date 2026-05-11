# TODO.md — CodeEnhancer Comparative Study
> Son güncelleme: 2026-05-11
> Claude Code: Bu dosyayı yaptığın her değişiklikten sonra güncelle. Tamamlananları ✅, devam edenleri 🔄, bloke olanları 🔴 ile işaretle.

---

## 🚨 ACİL — Mid-Phase Report (3 gün içinde)

- ✅ GitHub fork URL'si CLAUDE.md'ye eklendi (https://github.com/Aliekinozcetin/CodeEnhancer)
- ✅ Repo local'de çalışıyor: `.venv/` kurulu, `source .venv/bin/activate`
- [ ] Tüm deneylerin validasyonunu çalıştır: `python3 code_validator.py`
- [ ] Validation bittikten sonra: `python3 analysis/compare_results.py && python3 analysis/visualize.py`
- [ ] Mid-phase report taslağını yaz (bölüm 1, 2, 3, 4, 5)
- [ ] GitHub'a düzenli commit at (commit geçmişi hoca tarafından izleniyor)

---

## 🧪 Deneyler — Devam Eden

### Deney Çalıştırma
- 🔄 Tüm deneylerin validasyonu çalışıyor (`python3 code_validator.py`)
- [ ] 150 prompt → final için

---

## 📊 Analiz & Değerlendirme

- [ ] Validation tamamlanınca `compare_results.py` çalıştır → karşılaştırma tablosu
- [ ] Validation tamamlanınca `visualize.py` çalıştır → 5 grafik
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

### Altyapı & Kurulum
- ✅ `.env` dosyası oluşturuldu, GOOGLE_API_KEY eklendi
- ✅ `.env.example` ve `.gitignore` oluşturuldu
- ✅ `requirements.txt` oluşturuldu (google-genai, ollama, python-dotenv, bandit, pylint, matplotlib, pandas)
- ✅ Python virtual environment kuruldu (`.venv/`)
- ✅ Ollama kuruldu, 3 model indirildi: llama3.1, deepseek-coder:6.7b, mistral:7b
- ✅ `experiments/` klasör yapısı: 9 kombinasyon (3 model × 3 strateji)
- ✅ `prompts/zero_shot.py`, `few_shot.py`, `chain_of_thought.py` yazıldı
- ✅ `analysis/compare_results.py` — karşılaştırma tabloları (Bandit hit rate, CWE kırılımı, model/strateji ortalamaları)
- ✅ `analysis/visualize.py` — 5 grafik (bar chart, heatmap, stacked bar)
- ✅ `code_generator.py` hardcoded API key kaldırıldı, Ollama multi-model runner'a dönüştürüldü
- ✅ `code_validator.py` OpenAI → Ollama'ya uyarlandı, Bandit + Pylint + LLM döngüsü

### Veri & Deneyler
- ✅ LLMSecEval veri seti indirildi (`data/llmseceval/`, 150 prompt, 18 CWE)
- ✅ 15 prompt seçildi: `data/select_prompts.py` + `data/mid_phase_prompts.json` (12 CWE, katmanlı örnekleme, seed=42)
- ✅ 135 kod dosyası üretildi (9 deney × 15 prompt, tümü success)

### Kararlar
- ✅ Model matrisi kesinleşti: Llama 3.1 8B + DeepSeek-Coder 6.7B + Mistral 7B (tümü Ollama)
- ✅ Prompt stratejileri: Zero-shot, Few-shot (3 örnek), Chain-of-Thought
- ✅ 15 prompt: CWE dağılımına göre katmanlı örnekleme (seed=42)
- ✅ Gemini kapsam dışı bırakıldı (rate limit sorunu, bkz. DECISIONS.md #005)

---

## 🔴 Bloke / Karar Bekleniyor

_(Şu an bloke eden karar yok)_
