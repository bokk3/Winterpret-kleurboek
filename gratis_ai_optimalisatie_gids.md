# 🎯 Slim & Gratis Genereren: Leonardo.ai & Microsoft Designer
### *Haal het maximale uit je gratis dagelijkse tokens en bewaar 100% karakterstijl!*

Met zowel **Leonardo.ai** als **Microsoft Designer** heb je een gouden combinatie in handen. Je hoeft geen euro uit te geven aan abonnementen als je deze instellingen volgt.

---

## ⚡ Deel 1: Leonardo.ai – Token-Optimalisatie (Van 10 naar 100+ platen per dag!)

Standaard verbruikt Leonardo veel tokens als premium opties aanstaan. Zet deze instellingen goed en je kunt met je 150 dagelijkse tokens **tot wel 75 tot 150 afbeeldingen per dag genereren**!

### 🔧 De Juiste Knoppen in Leonardo (Linker Zijbalk & Menu):

| Instelling | Kies deze optie | Waarom? |
| :--- | :--- | :--- |
| **Number of Images** | **1** of **2** | Standaard staat dit op 4 (kost 4× zoveel tokens). Zet het op 1 of 2. Als een prompt goed is, genereer je er pas meer. |
| **Alchemy** | **UIT (Toggle OFF)** | **Cruciaal:** Alchemy kost 8 tot 16 tokens per klik! Zonder Alchemy kost een generatie slechts **1 of 2 tokens**! |
| **PhotoReal** | **UIT (OFF)** | Dit is voor realistische foto's en vreet onnodig tokens. |
| **Model** | **Leonardo Lightning XL** of **Leonardo Diffusion XL** | Lightning XL is supersnel, levert strakke lijnen en kost slechts **1 token per plaat**. |
| **Image Dimensions** | `1:1` (1024 × 1024) | Exact vierkant voor ons 8.5" × 8.5" boek. |
| **Negative Prompt** | **AAN (Toggle ON)** | Vul hieronder de negatieve prompt in (zie hieronder). |

### 🚫 Negatieve Prompt voor Leonardo (Kopieer & Plak):
```text
shading, gray, grayscale, shadow, gradients, crosshatch, 3d render, photorealistic, color, messy lines, watermark, text, signature, complex background, blurry
```

### 🌟 Leonardo's Superkracht: Karakterconsistentie (Image Guidance)
Als je op Pagina 1 een beertje Bas en eendje Pip hebt die je mooi vindt:
1. Klik op die afbeelding en kies **"Use as Image Guidance"** (of upload hem bij Image Guidance).
2. Kies het tabblad **"Character Reference"** of **"Image to Image"**.
3. Zet de schuifregelaar (*Strength*) op **0.30 - 0.35**.
4. Vul nu de prompt in voor Pagina 2. Leonardo gebruikt nu automatisch hetzelfde snoetje, truitje en mutsje voor de volgende pagina!

---

## 🎨 Deel 2: Microsoft Designer (DALL-E 3) – Onbeperkt & Spelenderwijs

Microsoft Designer (via `designer.microsoft.com` of `bing.com/create`) werkt op de **DALL-E 3** engine.

### 💡 Hoe werken de gratis tokens in Microsoft Designer?
- Je krijgt **15 "Snelle Boosts"** per dag.
- **Het geheim van Microsoft Designer**: Als je 15 boosts op zijn, **stopt hij NIET**! Hij schakelt simpelweg over naar de gratis standaardmodus. Het duurt dan 20 seconden in plaats van 5 seconden, maar je kunt **onbeperkt blijven genereren**!
- Hij genereert altijd 4 varianten per prompt.

### ⚠️ Belangrijke Tip voor DALL-E 3 Prompts:
DALL-E 3 begrijpt geen computertags zoals `--ar 1:1` of `--no shading`. DALL-E 3 wil **gewone, duidelijke zinnen in natuurlijke taal**:
- **Doe niet**: `baby bear, cute, vector, --ar 1:1, --no shading`
- **Doe wel**: `A toddler coloring book page with thick bold black outlines on a pure white background. No shading, no gray, no colors. Centered composition showing a chubby baby teddy bear...`

---

## 🚀 De Beste Werkwijze (De "Hybride" Aanpak)

1. **Stap 1: Verken scènes in Microsoft Designer (Onbeperkt)**
   - Gebruik Designer om snel scènes uit te proberen. Omdat het onbeperkt gratis is, maakt het niet uit als een poging mislukt.
2. **Stap 2: Vergrendel je stijl in Leonardo (Met Image Guidance)**
   - Heb je de perfecte stijl van Bas & Pip te pakken? Upload die afbeelding in Leonardo als referentie.
   - Genereer in Leonardo met de zuinige instellingen (1 token per keer). Zo blijven alle 24 platen in exact dezelfde tekenstijl.
3. **Stap 3: Download & Bewaar**
   - Noem de downloads: `pagina_01.png`, `pagina_02.png`, etc.
   - Plaats ze in de map `images/` in jouw projectmap.
4. **Stap 4: Direct in je PDF gieten**
   - Open PowerShell en voer uit:
     ```powershell
     python scripts/build_coloring_book_pdf.py
     ```
   - Klaar! Jouw PDF bevat direct de echte platen in plaats van de placeholders, compleet met Nederlandse voorleeszinnetjes en kleurrijke omslag.
