# ❄️ Warme Winterpret met Beertje Bas & Eendje Pip
### *Vlaams Kleur- en Voorleesboek voor Peuters & Kleuters (3–5 Jaar)*

---

## 📁 Overzicht van de Bestanden

- **[nieuwe_cover_en_achterkant_concept.md](file:///c:/Users/Boris/Documents/antigravity/clever-newton/nieuwe_cover_en_achterkant_concept.md)**: 100% uniek, niet-geplagieerd omslagontwerp met Krea-prompts voor de voor- en achterkant.
- **[krea_prompts_gids.md](file:///c:/Users/Boris/Documents/antigravity/clever-newton/krea_prompts_gids.md)**: Visuele handleiding met alle 24 Krea-prompts (dikke lijnen, peutervriendelijk) en bijbehorende voorleestekstjes.
- **[krea_prompts_24_paginas.json](file:///c:/Users/Boris/Documents/antigravity/clever-newton/krea_prompts_24_paginas.json)**: JSON-bestand met alle 24 scènes voor geautomatiseerde workflows.
- **[scripts/build_coloring_book_pdf.py](file:///c:/Users/Boris/Documents/antigravity/clever-newton/scripts/build_coloring_book_pdf.py)**: Python build-script dat automatisch een 8.5" × 8.5" (300 DPI) PDF genereert voor Amazon KDP & Bol.com.
- **`images/`**: Map waarin je gegenereerde afbeeldingen plaatst (`pagina_01.png` t/m `pagina_24.png`).
- **`Warme_Winterpret_Kleurboek_KDP_Bol.pdf`**: De kant-en-klare PDF met titelpagina, colofon, enkelzijdige pagina's en kleurdiploma.

---

## 🚀 Hoe Maak je het Boek Compleet?

1. **Afbeeldingen genereren in Krea.ai**:
   - Gebruik de prompts uit [krea_prompts_gids.md](file:///c:/Users/Boris/Documents/antigravity/clever-newton/krea_prompts_gids.md).
   - Instellingen: **1:1 vierkant**, stijl **Line Art / Coloring Book**, model **Flux / SDXL**.
2. **Afbeeldingen opslaan**:
   - Sla de downloads op in de map `images/` met namen zoals:
     `pagina_01.png`, `pagina_02.png`, ..., `pagina_24.png`.
3. **PDF bouwen met één commando**:
   ```bash
   python scripts/build_coloring_book_pdf.py
   ```
4. **Klaar voor verkoop**:
   - Upload de gegenereerde PDF direct naar **Amazon KDP** of **Brave New Books (Bol.com)**!
