# TODO.md — CodeEnhancer Comparative Study
> Son güncelleme: 2026-05-13
> Claude Code: Bu dosyayı yaptığın her değişiklikten sonra güncelle. Tamamlananları ✅, devam edenleri 🔄, bloke olanları 🔴 ile işaretle.

---

## ✅ Mid-Phase Report — TAMAMLANDI

- ✅ GitHub fork URL'si CLAUDE.md'ye eklendi
- ✅ Repo local'de çalışıyor: `.venv/` kurulu
- ✅ Validasyon tamamlandı (9 kombinasyon × 15 prompt)
- ✅ `compare_results.py` → `analysis/comparison_report.json`
- ✅ `visualize.py` → 5 grafik (`analysis/figures/`)
- ✅ Branch A raporu: `report/my_report.tex`
- ✅ Harmanlanmış rapor: `report/shared/main.tex` (5 model, 2 branch)
- 🔄 GitHub commit geçmişi aktif tutulyor

---

## 🧪 Deneyler — Devam Eden

### Deney Çalıştırma
- ✅ 15 prompt × 9 kombinasyon validasyonu tamamlandı
- [ ] 150 prompt → final için (gece batch çalıştırma planlanıyor)

---

## 📊 Analiz & Değerlendirme

- ✅ `compare_results.py` çalıştırıldı → karşılaştırma tablosu üretildi
- ✅ `visualize.py` çalıştırıldı → 5 grafik üretildi
- [ ] En az 5 başarısız örnek seç → nitel hata analizi yaz (final için)

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
