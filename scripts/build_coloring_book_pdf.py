import os
import json
from PIL import Image, ImageDraw, ImageFont

# Constanten voor KDP & Bol.com (8.5 x 8.5 inch bij 300 DPI)
DPI = 300
PAGE_WIDTH = int(8.5 * DPI)   # 2550 pixels
PAGE_HEIGHT = int(8.5 * DPI)  # 2550 pixels
MARGIN = int(0.5 * DPI)       # 150 pixels veiligheidsmarge

def get_font(size, bold=False):
    """Laadt een schoon Windows systeemfont of valt terug op het standaardfont."""
    font_names = [
        "C:\\Windows\\Fonts\\comic.ttf" if not bold else "C:\\Windows\\Fonts\\comicbd.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf" if not bold else "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arial.ttf" if not bold else "C:\\Windows\\Fonts\\arialbd.ttf"
    ]
    for path in font_names:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_corner_snowflakes(draw, width, height, margin=80):
    """Tekent subtiele decoratieve sneeuwvlokjes in de hoeken van de pagina."""
    def snowflake(x, y, r=25):
        draw.line([(x - r, y), (x + r, y)], fill=(180, 180, 180), width=4)
        draw.line([(x, y - r), (x, y + r)], fill=(180, 180, 180), width=4)
        draw.line([(x - r*0.7, y - r*0.7), (x + r*0.7, y + r*0.7)], fill=(180, 180, 180), width=3)
        draw.line([(x - r*0.7, y + r*0.7), (x + r*0.7, y - r*0.7)], fill=(180, 180, 180), width=3)

    snowflake(margin + 50, margin + 50)
    snowflake(width - margin - 50, margin + 50)
    snowflake(margin + 50, height - margin - 50)
    snowflake(width - margin - 50, height - margin - 50)

def create_title_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT)
    
    font_title = get_font(130, bold=True)
    font_sub = get_font(65, bold=False)
    font_tag = get_font(50, bold=True)
    
    title_text = "Warme Winterpret"
    sub_text = "met Beertje Bas & Eendje Pip"
    tag_text = "Een knus kleur- en voorleesboek voor peuters & kleuters (3-5 jaar)"
    
    # Tekst centreren
    draw.text((PAGE_WIDTH // 2, 800), title_text, fill=(30, 30, 30), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 980), sub_text, fill=(60, 60, 60), font=font_sub, anchor="mm")
    
    # Decoratieve lijn
    draw.line([(PAGE_WIDTH // 2 - 400, 1100), (PAGE_WIDTH // 2 + 400, 1100)], fill=(100, 100, 100), width=6)
    
    draw.text((PAGE_WIDTH // 2, 1250), tag_text, fill=(80, 80, 80), font=font_tag, anchor="mm")
    
    # Kadertje voor naam
    name_box_y = 1700
    draw.rounded_rectangle(
        [(PAGE_WIDTH // 2 - 600, name_box_y), (PAGE_WIDTH // 2 + 600, name_box_y + 300)],
        radius=30, outline=(120, 120, 120), width=5
    )
    font_name = get_font(55, bold=False)
    draw.text((PAGE_WIDTH // 2, name_box_y + 70), "Dit vrolijke kleurboek is van:", fill=(80, 80, 80), font=font_name, anchor="mm")
    draw.line([(PAGE_WIDTH // 2 - 500, name_box_y + 200), (PAGE_WIDTH // 2 + 500, name_box_y + 200)], fill=(150, 150, 150), width=3)
    
    return img

def create_colophon_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_body = get_font(36, bold=False)
    font_small = get_font(28, bold=False)
    
    colophon_lines = [
        "Warme Winterpret met Beertje Bas & Eendje Pip",
        "Eerste Druk - 2026",
        "",
        "Tekst & Illustratieconcept: Eigen Uitgave",
        "Geoptimaliseerd voor Amazon KDP & Bol.com",
        "",
        "Alle rechten voorbehouden.",
        "Niets uit deze uitgave mag worden verveelvoudigd zonder voorafgaande toestemming.",
        "",
        "Gedrukt op milieuvriendelijk papier via Print-on-Demand."
    ]
    
    y = 1100
    for line in colophon_lines:
        draw.text((PAGE_WIDTH // 2, y), line, fill=(100, 100, 100), font=font_body, anchor="mm")
        y += 60
        
    return img

def create_coloring_page(page_data, images_dir):
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    page_num = page_data["page"]
    voorleestekst = page_data["voorleestekst"]
    title = page_data["title"]
    
    # 1. Kleurplaat Afbeelding Laden of Placeholder Maken
    image_filename = f"pagina_{page_num:02d}.png"
    image_path = os.path.join(images_dir, image_filename)
    if not os.path.exists(image_path):
        image_path = os.path.join(images_dir, f"pagina_{page_num:02d}.jpg")
    
    # Bepaal het vak voor de tekening (bovenste 72% van de pagina)
    art_box_x1 = MARGIN + 80
    art_box_y1 = MARGIN + 60
    art_box_x2 = PAGE_WIDTH - MARGIN - 80
    art_box_y2 = int(PAGE_HEIGHT * 0.72)
    art_box_w = art_box_x2 - art_box_x1
    art_box_h = art_box_y2 - art_box_y1
    
    if os.path.exists(image_path):
        try:
            art = Image.open(image_path).convert("RGB")
            art = art.resize((art_box_w, art_box_h), Image.Resampling.LANCZOS)
            img.paste(art, (art_box_x1, art_box_y1))
            # Afgerond kader rond de illustratie
            draw.rounded_rectangle([(art_box_x1, art_box_y1), (art_box_x2, art_box_y2)], radius=25, outline=(0, 0, 0), width=6)
        except Exception as e:
            print(f"Kon afbeelding {image_path} niet laden: {e}")
    else:
        # Teken een mooie placeholder voor testdoeleinden
        draw.rounded_rectangle([(art_box_x1, art_box_y1), (art_box_x2, art_box_y2)], radius=25, outline=(40, 40, 40), width=8)
        font_ph_title = get_font(70, bold=True)
        font_ph_sub = get_font(42, bold=False)
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 400), f"Kleurplaat {page_num}", fill=(50, 50, 50), font=font_ph_title, anchor="mm")
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 520), f"« {title} »", fill=(80, 80, 80), font=font_ph_sub, anchor="mm")
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 750), f"[ Plaats hier je Krea-afbeelding: images/pagina_{page_num:02d}.png ]", fill=(140, 140, 140), font=font_ph_sub, anchor="mm")
        draw_corner_snowflakes(draw, PAGE_WIDTH, int(PAGE_HEIGHT * 0.75), margin=180)

    # 2. Voorleesvak onderaan de pagina
    text_box_y1 = int(PAGE_HEIGHT * 0.76)
    text_box_y2 = PAGE_HEIGHT - MARGIN - 70
    draw.rounded_rectangle(
        [(art_box_x1, text_box_y1), (art_box_x2, text_box_y2)],
        radius=25, outline=(180, 180, 180), width=4
    )
    
    # Titel van het verhaaltje
    font_story_title = get_font(46, bold=True)
    draw.text((PAGE_WIDTH // 2, text_box_y1 + 65), f"❄️ {title}", fill=(40, 40, 40), font=font_story_title, anchor="mm")
    
    # Voorleestekst met automatische regelafbreking
    font_story_text = get_font(42, bold=False)
    
    words = voorleestekst.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        # ruwe schatting breedte
        if len(test_line) > 52:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(" ".join(current_line))
        
    line_y = text_box_y1 + 150
    for line in lines:
        draw.text((PAGE_WIDTH // 2, line_y), line, fill=(50, 50, 50), font=font_story_text, anchor="mm")
        line_y += 65
        
    # Paginanummer
    font_pg = get_font(36, bold=False)
    draw.text((PAGE_WIDTH // 2, PAGE_HEIGHT - 60), f"- {page_num} -", fill=(120, 120, 120), font=font_pg, anchor="mm")
    
    return img

def create_blank_back_page():
    """Maakt een blanco linkerpagina aan om doordrukken van viltstiften te voorkomen."""
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Lichte sneeuwvlokjes op de achterkant als zacht watermerk
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=150)
    font_note = get_font(32, bold=False)
    draw.text((PAGE_WIDTH // 2, PAGE_HEIGHT - 120), "❄️ Ruimte om je eigen wintertekening te maken! ❄️", fill=(200, 200, 200), font=font_note, anchor="mm")
    return img

def create_diploma_page():
    """Kleurdiploma aan het einde van het boek."""
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle([(MARGIN + 50, MARGIN + 50), (PAGE_WIDTH - MARGIN - 50, PAGE_HEIGHT - MARGIN - 50)], radius=40, outline=(30, 30, 30), width=10)
    draw.rounded_rectangle([(MARGIN + 75, MARGIN + 75), (PAGE_WIDTH - MARGIN - 75, PAGE_HEIGHT - MARGIN - 75)], radius=35, outline=(150, 150, 150), width=4)
    
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=120)
    
    font_dip_title = get_font(120, bold=True)
    font_dip_sub = get_font(55, bold=False)
    font_dip_name = get_font(65, bold=True)
    
    draw.text((PAGE_WIDTH // 2, 700), "⭐ KLEURDIPLOMA ⭐", fill=(20, 20, 20), font=font_dip_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 880), "Hoera! Dit officiële winterdiploma is voor:", fill=(70, 70, 70), font=font_dip_sub, anchor="mm")
    
    # Naamlijn
    draw.line([(PAGE_WIDTH // 2 - 600, 1150), (PAGE_WIDTH // 2 + 600, 1150)], fill=(80, 80, 80), width=4)
    draw.text((PAGE_WIDTH // 2, 1100), "( Naam van de kunstenaar )", fill=(170, 170, 170), font=font_dip_sub, anchor="mm")
    
    draw.text((PAGE_WIDTH // 2, 1380), "Omdat jij alle avonturen van Beertje Bas & Eendje Pip", fill=(50, 50, 50), font=font_dip_sub, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 1460), "zo prachtig hebt ingekleurd!", fill=(50, 50, 50), font=font_dip_sub, anchor="mm")
    
    # Handtekening Bas & Pip
    draw.text((PAGE_WIDTH // 2, 1750), "Pootje van Bas 🐾  &  Vleugeltje van Pip 🦆", fill=(60, 60, 60), font=font_dip_name, anchor="mm")
    
    return img

def build_pdf():
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(workspace, "krea_prompts_24_paginas.json")
    images_dir = os.path.join(workspace, "images")
    output_pdf = os.path.join(workspace, "Warme_Winterpret_Kleurboek_KDP_Bol.pdf")
    
    os.makedirs(images_dir, exist_ok=True)
    
    with open(json_path, "r", encoding="utf-8") as f:
        pages_data = json.load(f)
        
    print(f"Samenstellen van kleurboek (8.5 x 8.5 inch @ 300 DPI, enkelzijdig)...")
    pages = []
    
    # 1. Titelpagina
    print("- Titelpagina aanmaken...")
    pages.append(create_title_page())
    
    # 2. Colofon / Blanco
    print("- Colofonpagina aanmaken...")
    pages.append(create_colophon_page())
    
    # 3. 24 Kleurplaten (enkelzijdig: Kleurplaat rechts, blanco links)
    blank_back = create_blank_back_page()
    for p in pages_data:
        print(f"- Pagina {p['page']}/24: {p['title']}")
        coloring_page = create_coloring_page(p, images_dir)
        pages.append(coloring_page)
        pages.append(blank_back) # Blanco achterzijde ter bescherming van stiften
        
    # 4. Kleurdiploma
    print("- Kleurdiploma aanmaken...")
    pages.append(create_diploma_page())
    pages.append(blank_back)
    
    print(f"Totaal aantal pagina's in PDF: {len(pages)}")
    print(f"Opslaan naar {output_pdf}...")
    pages[0].save(
        output_pdf,
        save_all=True,
        append_images=pages[1:],
        resolution=300.0,
        quality=95
    )
    print(f"[OK] Klaar! PDF succesvol gegenereerd: {output_pdf}")

if __name__ == "__main__":
    build_pdf()
