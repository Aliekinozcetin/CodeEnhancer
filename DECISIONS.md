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

### #005 — Model Seçimi (Final)
**Tarih:** 2026-05-11 → Final revize: 2026-05-11
**Durum:** ✅ Kesinleşti
**Karar:** Deney matrisi: **Llama 3.1 8B** (Meta, genel), **DeepSeek-Coder 6.7B** (DeepSeek, kod-özelleşmiş), **Mistral 7B** (Mistral AI, genel) — tümü Ollama üzerinden local çalışır, ücretsiz.
**Gerekçe:** Gemini API free tier yeni key'lerde aktif olmuyor (429 RESOURCE_EXHAUSTED). Tamamen local Ollama modelleriyle devam edildi. Llama 3.1 8B (Meta, genel) vs DeepSeek-Coder 6.7B (kod-özelleşmiş) vs Mistral 7B (Avrupa, genel) → farklı provider + genel vs kod-özelleşmiş karşılaştırması akademik olarak güçlü argüman sağlar. M4 + 16GB RAM ile tüm modeller Metal GPU'da hızlı çalışır.
**Reddedilen Alternatifler:** Gemini modelleri (API key rate limit sorunu), GPT-4o (ücretli), Phi-4 Mini (model boyutu etkisi ayrı tez konusu), CodeGemma (arkadaş kullanıyor, çakışma).
**Etkisi:** `code_generator.py`'e Gemini client + Ollama REST API client entegre edilecek. Deney klasörleri güncellendi.

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

### #009 — Çok-Branch Karşılaştırması için Ortak Bileşenler
**Tarih:** 2026-05-11
**Durum:** ✅ Kesinleşti
**Karar:** Farklı branch/takımların sonuçları akademik olarak karşılaştırılabilir olması için aşağıdaki bileşenler **birebir aynı** olmalıdır. Bu bileşenler değiştirilmeden diğer branch'e kopyalanmalı veya ortak bir repo'dan çekilmelidir.

**Kesinlikle ortak tutulacaklar (kontrol değişkeni — farklılaşırsa karşılaştırma geçersiz olur):**

| Dosya / Parametre | Neden kritik |
|---|---|
| `data/mid_phase_prompts.json` | Aynı 15 prompt, aynı ID'ler — farklı prompt seti ile model karşılaştırması anlamsızlaşır |
| `data/select_prompts.py` | Seed=42, aynı CWE dağılımı — tekrarlanabilirlik için |
| `prompts/zero_shot.py` | Prompt metni farklılaşırsa model performansı değil prompt performansı ölçülür |
| `prompts/few_shot.py` | Aynı 3 örnek (CWE-78, CWE-89, CWE-502), aynı format |
| `prompts/chain_of_thought.py` | Aynı adım yapısı (Step 1–4) |
| `code_validator.py` — SAST mantığı ve `MAX_ATTEMPTS=5` | Farklı iterasyon limiti veya Bandit parametresi → metrikler kıyaslanamaz |
| `analysis/compare_results.py` — metrik formülleri | Farklı hesap yöntemi → farklı sonuç, aynı veriyle |

**Kasıtlı farklı olacaklar (bağımsız değişken — zaten farklı olması beklenir):**

| Dosya | Neden farklı olabilir |
|---|---|
| `code_generator.py` — MODEL_IDS, EXPERIMENTS | Her branch farklı modelleri test ediyor |
| `experiments/` klasörleri | Her branch kendi model çıktılarını barındırır |
| `analysis/visualize.py` | Görsel tercih, akademik sonucu etkilemez |

**Gerekçe:** Kontrol edilemeyen değişken (confound) olmadan "hangi model daha iyi güvenlik kodu üretiyor" sorusunu yanıtlamak için veri seti, prompt tasarımı, SAST parametreleri ve metrik hesabının tüm gruplarda aynı olması temel araştırma metodolojisi gereğidir.
**Etkisi:** Diğer branch bu dosyaları bu repo'dan doğrudan almalı veya senkronize tutmalıdır.

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
| C1 | API maliyeti — tüm modeller ücretsiz Gemini'ye geçildi, maliyet sıfır | Yüksek | ✅ Kapandı |
| C2 | LLMSecEval veri setine erişim — GitHub'dan doğrudan indirilebilir mi? | Orta | ✅ Kapandı — indirildi |
| C3 | Farklı API'lerin rate limit'leri — paralel çalıştırmada sorun çıkabilir | Orta | ✅ Kapandı — tamamen Ollama'ya geçildi |
| C4 | Bandit'in false positive oranı — bazı "güvenli" kodları zafiyet olarak işaretleyebilir | Düşük | Açık |
| C5 | Commit geçmişi — hoca izliyor, mid-phase'e kadar düzenli commit şart | Yüksek | Açık |
