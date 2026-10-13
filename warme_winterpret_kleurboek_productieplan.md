# ❄️ Warme Winterpret met Beertje Bas & Eendje Pip
### *Compleet Productie-, Schrijf- en Publicatiepakket (3–5 Jaar)*

---

## 🎨 1. De Voltooide Omslag (Nederlandse Voor- en Achterkant)

De voor- en achterkant zijn volledig in het Nederlands bewerkt, inclusief typografie en afwerking:

- **Voorkant**: `covers/front_cover_nl.jpg` (*WARME WINTERPRET - Knus & Vrolijk Kleuren*)
- **Achterkant**: `covers/back_cover_nl.jpg` (*WARME WINTERPRET - 24 Vrolijke Winterplaten om in te kleuren!*)

---

## 📄 2. Gegenereerde PDF Bestanden

In jouw projectmap staan twee kant-en-klare PDF's gereed:

1. **[Warme_Winterpret_Kleurboek_KDP_Bol.pdf](file:///c:/Users/Boris/Documents/antigravity/clever-newton/Warme_Winterpret_Kleurboek_KDP_Bol.pdf)** *(55 Pagina's)*
   - **Pagina 1**: Kleurrijke Voorkant (Front Cover)
   - **Pagina 2**: Blanco binnenkant
   - **Pagina 3**: Titelpagina (*Warme Winterpret met Bas & Pip*)
   - **Pagina 4**: Colofon & *"Dit boekje is van: ..."*
   - **Pagina 5 t/m 52**: 24 Enkelzijdige kleurplaten met Vlaamse voorleestekst (rechterpagina) en blanco beschermpagina's met sneeuwvlokjes (linkerpagina).
   - **Pagina 53**: Officieel Winter-Kleurdiploma voor peuters.
   - **Pagina 54**: Blanco pagina
   - **Pagina 55**: Kleurrijke Achterkant (Back Cover)
2. **[Warme_Winterpret_Cover_Spread_KDP.pdf](file:///c:/Users/Boris/Documents/antigravity/clever-newton/Warme_Winterpret_Cover_Spread_KDP.pdf)**
   - De officiële **Full Wrap Cover** (Achterkant + Rugdikte + Voorkant + 0.125" afloop/bleed) die Amazon KDP en Bol.com vereisen als apart cover-bestand voor paperback printing!

---

## 💡 3. Geen Krea Abonnement? Zo Genereer je Alles 100% Gratis!

Je hebt **geen betaald Krea-abonnement** nodig om de 24 pagina's te maken. Hier zijn de beste opties:

### Optie 1: Krea.ai Gratis Account
- Krea heeft een gratis versie: maak een account aan op [krea.ai](https://www.krea.ai).
- Je krijgt dagelijks gratis generatie-credits. Je kunt dus elke dag een paar platen gratis genereren met de prompts uit [krea_prompts_gids.md](file:///c:/Users/Boris/Documents/antigravity/clever-newton/krea_prompts_gids.md)!

### Optie 2: Microsoft Designer / Bing Image Creator (DALL-E 3) – 100% Gratis
- Ga naar **[bing.com/create](https://www.bing.com/create)** of **[designer.microsoft.com](https://designer.microsoft.com)**.
- Volledig gratis met een Microsoft-account.
- Plak direct de prompts uit [krea_prompts_gids.md](file:///c:/Users/Boris/Documents/antigravity/clever-newton/krea_prompts_gids.md). DALL-E 3 genereert haarscherpe, peutervriendelijke zwart-wit lijntekeningen met dikke lijnen.

### Optie 3: Leonardo.ai – 150 Gratis Credits per Dag
- Ga naar **[leonardo.ai](https://leonardo.ai)**.
- Je ontvangt elke 24 uur automatisch 150 gratis snelle tokens (goed voor ca. 20-30 kleurplaten per dag). Binnen 1 à 2 dagen heb je het complete boek gratis klaar!

---

## 🛠️ 4. Hoe Werkt het Script?

Zodra je een afbeelding downloadt:
1. Sla hem op in de map `images/` als:
   `pagina_01.png`, `pagina_02.png`, ..., `pagina_24.png`.
2. Voer in de terminal uit:
   ```powershell
   python scripts/build_coloring_book_pdf.py
   ```
3. Het script vervangt automatisch de placeholders door jouw echte tekeningen, behoudt de Vlaamse voorleesteksten, en levert direct de definitieve PDF af!
