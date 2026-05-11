# DECISIONS.md — Kararlar ve Gerekçeler
> Son güncelleme: 2026-05-11
> Claude Code: Bir karar alındığında veya reddedildiğinde buraya ekle. Format: Karar ID, tarih, karar, gerekçe, alternatifler.

---

## Karar Formatı

```
### #XXX — [Karar Başlığı]
**Tarih:** YYYY-MM-DD
**Durum:** ✅ Kesinleşti / 🔄 Tartışılıyor / ❌ Reddedildi
**Karar:** ...
**Gerekçe:** ...
**Reddedilen Alternatifler:** ...
**Etkisi:** Hangi dosyalar/scriptler değişecek?
```

---

## Kesinleşmiş Kararlar

### #001 — Stage 2 (Fine-Tuning) Kapsam Dışı
**Tarih:** Proje başlangıcı
**Durum:** ✅ Kesinleşti
**Karar:** Fine-tuning aşaması (CodeEnhancer Stage 2) uygulanmayacak.
**Gerekçe:** Hoca direktifi — ders projesi için süre kısıtlı, Stage 1 yeterli. Fine-tuning ayrıca hesaplama maliyeti açısından da uygun değil.
**Reddedilen Alternatifler:** QLoRA ile hafif fine-tuning (kapsam dışı bırakıldı).
**Etkisi:** `code_validator.py`'nin ürettiği eğitim verisi kullanılmayacak.

---

### #002 — Temel Framework: CodeEnhancer Stage 1
**Tarih:** Proje başlangıcı
**Durum:** ✅ Kesinleşti
**Karar:** Orijinal CodeEnhancer repo'su fork'lanacak, Stage 1 pipeline'ı korunacak ve üzerine çoklu model + prompt desteği eklenecek.
**Gerekçe:** Çalışan bir baseline var, sıfırdan yazmak zaman kaybı. Fork üzerine genişletmek hem tekrarlanabilirlik hem de akademik dürüstlük açısından doğru.
**Reddedilen Alternatifler:** Sıfırdan pipeline yazmak — gereksiz, riskli.
**Etkisi:** `code_generator.py` ve `code_validator.py` refactor edilecek, prompt stratejisi parametre olarak geçilebilir hale getirilecek.

---

### #003 — Veri Seti: LLMSecEval
**Tarih:** Proje başlangıcı
**Durum:** ✅ Kesinleşti
**Karar:** LLMSecEval kullanılacak (150 prompt, CWE Top 25).
**Gerekçe:** Orijinal CodeEnhancer makalesinde de kullanılmış — bu sayede baseline karşılaştırması doğrudan yapılabilir. SecurityEval (121 prompt, 69 CWE) ise cross-dataset validasyon için opsiyonel tutulacak.
**Reddedilen Alternatifler:** SecurityEval tek başına — CWE Top 25 karşılaştırması kısıtlanırdı.
**Etkisi:** `data/llmseceval/` klasörü oluşturulacak.

---

### #004 — Deney İzolasyonu: `experiments/` Klasör Yapısı
**Tarih:** Proje başlangıcı
**Durum:** ✅ Kesinleşti
**Karar:** Her model × prompt stratejisi kombinasyonu `experiments/<model>_<strateji>/` altında ayrı klasörde tutulacak.
**Gerekçe:** Sonuçların karışmaması, her kombinasyonun bağımsız tekrarlanabilmesi ve karşılaştırma scriptinin kolayca çalışabilmesi için.
**Reddedilen Alternatifler:** Tek `baseline/` klasörü kullanmak — orijinal repo yapısı, birden fazla deneye uygun değil.
**Etkisi:** `code_generator.py` ve `code_validator.py`'de `BASE_DIR` parametresi dışarıdan set edilebilir olacak.

---

## Tartışılıyor / Karar Bekleniyor

_(Şu an bekleyen karar yok)_

---

## Kesinleşmiş Kararlar (Devam)

### #005 — Model Seçimi (Final — Revize 2)
**Tarih:** 2026-05-11 → Revize 2: 2026-05-11
**Durum:** ✅ Kesinleşti
**Karar:** Tüm modeller **Ollama** üzerinden local çalışacak. Deney matrisi: **Qwen2.5-Coder 7B** (kod-uzmanı), **Llama 3.1 8B** (genel amaçlı baseline), **Gemma 2 9B** (farklı vendor/mimari). OpenAI ve Google API kapsam dışı.
**Gerekçe:** (1) Sıfır API maliyeti — tüm deneyler local. (2) Tam tekrarlanabilirlik — cloud API davranışı zamanla değişebilir, local model sabittir. (3) Üç farklı vendor (Alibaba, Meta, Google) = farklı eğitim verisi ve bias. (4) Kod-uzmanı vs genel amaçlı karşılaştırması güçlü bir araştırma sorusu: "Kod-uzmanı model, güvenlik açıklarını genel amaçlı modellerden daha iyi önler mi?"
**Reddedilen Alternatifler:** Gemini API (cloud bağımlılığı, rate limit riski), GPT-4o (ücretli), Claude (ücretli), Mistral 7B (Gemma 2 9B daha güncel ve daha iyi benchmark sonuçları).
**Etkisi:** `code_generator.py` ve `code_validator.py` Ollama OpenAI-compat endpoint kullanacak. `.env` güncellendi. Deney klasörleri yeniden oluşturuldu.

---

### #006 — Few-Shot Örnek Sayısı
**Tarih:** 2026-05-11
**Durum:** ✅ Kesinleşti
**Karar:** 3 örnek kullanılacak.
**Gerekçe:** Literatürde standart (Brown et al., 2020 GPT-3 few-shot çalışması başta), token maliyeti ile performans arasında dengeli seçim.
**Reddedilen Alternatifler:** 2 örnek (yetersiz sinyal), 5 örnek (yüksek maliyet × 150 prompt × 3 model).
**Etkisi:** `prompts/few_shot.py` şablonunda 3 örnek yer alacak.

---

### #007 — Mid-Phase İçin 15 Prompt Seçimi
**Tarih:** 2026-05-11
**Durum:** ✅ Kesinleşti
**Karar:** CWE dağılımına göre katmanlı örnekleme yapılacak — her temsil edilen CWE kategorisinden en az 1 prompt seçilecek, 15 prompta tamamlanacak.
**Gerekçe:** Nitel hata analizinde "hangi zafiyet tipi hangi modele dirençli" sorusunu yanıtlamak için temsili dağılım şart. Rastgele seçim bu soruyu cevaplamayı zorlaştırır.
**Reddedilen Alternatifler:** Rastgele 15 (temsil gücü belirsiz).
**Etkisi:** `data/select_prompts.py` scripti yazılacak, seçilen 15 prompt `data/mid_phase_prompts.json`'a kaydedilecek.

---

## Reddedilen Kararlar

### #008 — Donanım Optimizasyonu (AWQ, Quantization)
**Tarih:** Proje başlangıcı
**Durum:** ❌ Reddedildi
**Gerekçe:** Hoca direktifi — ders kapsamı ve süre dışında. Araştırma raporunda referans verilebilir ama uygulanmayacak.

---

## Açık Endişeler

| ID | Endişe | Öncelik | Durum |
|----|--------|---------|-------|
| C1 | API maliyeti — tüm modeller Ollama local, maliyet sıfır | Yüksek | ✅ Kapandı |
| C2 | LLMSecEval veri setine erişim — GitHub'dan doğrudan indirilebilir mi? | Orta | Açık |
| C3 | ~~Farklı API'lerin rate limit'leri~~ — Ollama local, rate limit yok | Orta | ✅ Kapandı |
| C4 | Bandit'in false positive oranı — bazı "güvenli" kodları zafiyet olarak işaretleyebilir | Düşük | Açık |
| C5 | Commit geçmişi — hoca izliyor, mid-phase'e kadar düzenli commit şart | Yüksek | Açık |
| C6 | Ollama RAM kullanımı — 16 GB RAM'de 9B model + OS overhead sınırda olabilir | Orta | Açık |
