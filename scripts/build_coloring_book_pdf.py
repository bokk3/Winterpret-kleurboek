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

def load_or_create_cover(cover_path, is_back=False):
    """Laadt een coverafbeelding en schaalt deze naar 300 DPI 8.5x8.5 inch."""
    if os.path.exists(cover_path):
        img = Image.open(cover_path).convert("RGB")
        return img.resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    else:
        img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(200, 220, 240))
        draw = ImageDraw.Draw(img)
        font = get_font(90, bold=True)
        text = "VOORKANT" if not is_back else "ACHTERKANT"
        draw.text((PAGE_WIDTH // 2, PAGE_HEIGHT // 2), text, fill=(30, 30, 30), font=font, anchor="mm")
        return img

def create_title_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT)
    
    font_title = get_font(130, bold=True)
    font_sub = get_font(65, bold=False)
    font_tag = get_font(48, bold=True)
    
    title_text = "Warme Winterpret"
    sub_text = "met Beertje Bas & Eendje Pip"
    tag_text = "Een knus kleur- en voorleesboek voor peuters & kleuters (3-5 jaar)"
    
    draw.text((PAGE_WIDTH // 2, 750), title_text, fill=(30, 30, 30), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 930), sub_text, fill=(60, 60, 60), font=font_sub, anchor="mm")
    
    draw.line([(PAGE_WIDTH // 2 - 400, 1060), (PAGE_WIDTH // 2 + 400, 1060)], fill=(120, 150, 180), width=6)
    draw.text((PAGE_WIDTH // 2, 1180), tag_text, fill=(80, 80, 80), font=font_tag, anchor="mm")
    
    # Kadertje voor naam
    name_box_y = 1650
    draw.rounded_rectangle(
        [(PAGE_WIDTH // 2 - 600, name_box_y), (PAGE_WIDTH // 2 + 600, name_box_y + 320)],
        radius=30, outline=(120, 150, 180), width=5
    )
    font_name = get_font(52, bold=False)
    draw.text((PAGE_WIDTH // 2, name_box_y + 80), "Dit vrolijke kleurboek is van:", fill=(70, 70, 70), font=font_name, anchor="mm")
    draw.line([(PAGE_WIDTH // 2 - 450, name_box_y + 220), (PAGE_WIDTH // 2 + 450, name_box_y + 220)], fill=(160, 160, 160), width=3)
    
    return img

def create_colophon_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_body = get_font(36, bold=False)
    
    colophon_lines = [
        "Warme Winterpret met Beertje Bas & Eendje Pip",
        "Eerste Druk - 2026",
        "",
        "Tekst & Illustratieconcept: Eigen Uitgave",
        "Geoptimaliseerd voor Amazon KDP & Bol.com",
        "Vlaams Nederlands - Doelgroep 3 tot 5 jaar",
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
    
    # 1. Zoek naar gegenereerde afbeelding
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
            draw.rounded_rectangle([(art_box_x1, art_box_y1), (art_box_x2, art_box_y2)], radius=25, outline=(0, 0, 0), width=6)
        except Exception as e:
            print(f"Kon afbeelding {image_path} niet laden: {e}")
    else:
        # Schone peutervriendelijke placeholder
        draw.rounded_rectangle([(art_box_x1, art_box_y1), (art_box_x2, art_box_y2)], radius=25, outline=(30, 30, 30), width=8)
        font_ph_title = get_font(70, bold=True)
        font_ph_sub = get_font(42, bold=False)
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 380), f"Kleurplaat {page_num}", fill=(50, 50, 50), font=font_ph_title, anchor="mm")
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 500), f"« {title} »", fill=(70, 70, 70), font=font_ph_sub, anchor="mm")
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 720), f"[ Sla je AI-tekening op als: images/pagina_{page_num:02d}.png ]", fill=(140, 140, 140), font=font_ph_sub, anchor="mm")
        draw_corner_snowflakes(draw, PAGE_WIDTH, int(PAGE_HEIGHT * 0.75), margin=180)

    # 2. Voorleesvak onderaan de pagina
    text_box_y1 = int(PAGE_HEIGHT * 0.76)
    text_box_y2 = PAGE_HEIGHT - MARGIN - 70
    draw.rounded_rectangle(
        [(art_box_x1, text_box_y1), (art_box_x2, text_box_y2)],
        radius=25, outline=(180, 180, 180), width=4
    )
    
    font_story_title = get_font(46, bold=True)
    draw.text((PAGE_WIDTH // 2, text_box_y1 + 65), f"❄️ {title}", fill=(40, 40, 40), font=font_story_title, anchor="mm")
    
    font_story_text = get_font(42, bold=False)
    words = voorleestekst.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
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
        
    font_pg = get_font(36, bold=False)
    draw.text((PAGE_WIDTH // 2, PAGE_HEIGHT - 60), f"- {page_num} -", fill=(120, 120, 120), font=font_pg, anchor="mm")
    
    return img

def create_blank_back_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=150)
    font_note = get_font(32, bold=False)
    draw.text((PAGE_WIDTH // 2, PAGE_HEIGHT - 120), "❄️ Ruimte om je eigen wintertekening te maken! ❄️", fill=(200, 200, 200), font=font_note, anchor="mm")
    return img

def create_diploma_page():
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
    
    draw.line([(PAGE_WIDTH // 2 - 600, 1150), (PAGE_WIDTH // 2 + 600, 1150)], fill=(80, 80, 80), width=4)
    draw.text((PAGE_WIDTH // 2, 1100), "( Naam van de kunstenaar )", fill=(170, 170, 170), font=font_dip_sub, anchor="mm")
    
    draw.text((PAGE_WIDTH // 2, 1380), "Omdat jij alle avonturen van Beertje Bas & Eendje Pip", fill=(50, 50, 50), font=font_dip_sub, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 1460), "zo prachtig hebt ingekleurd!", fill=(50, 50, 50), font=font_dip_sub, anchor="mm")
    
    draw.text((PAGE_WIDTH // 2, 1750), "Pootje van Bas 🐾  &  Vleugeltje van Pip 🦆", fill=(60, 60, 60), font=font_dip_name, anchor="mm")
    
    return img

def build_pdf():
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(workspace, "krea_prompts_24_paginas.json")
    images_dir = os.path.join(workspace, "images")
    covers_dir = os.path.join(workspace, "covers")
    output_pdf = os.path.join(workspace, "Warme_Winterpret_Kleurboek_KDP_Bol.pdf")
    output_cover_spread = os.path.join(workspace, "Warme_Winterpret_Cover_Spread_KDP.pdf")
    
    front_cover_path = os.path.join(covers_dir, "front_cover_nl.jpg")
    back_cover_path = os.path.join(covers_dir, "back_cover_nl.jpg")
    
    os.makedirs(images_dir, exist_ok=True)
    
    with open(json_path, "r", encoding="utf-8") as f:
        pages_data = json.load(f)
        
    print("Samenstellen van kleurboek (8.5 x 8.5 inch @ 300 DPI, enkelzijdig)...")
    pages = []
    
    # 1. Kleurrijke Voorkant Omslag
    print("- Voorkant toevoegen (in kleur)...")
    front_cover = load_or_create_cover(front_cover_path, is_back=False)
    pages.append(front_cover)
    
    # 2. Binnenkant voorblad (blanco)
    blank_page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    pages.append(blank_page)
    
    # 3. Titelpagina
    print("- Titelpagina aanmaken...")
    pages.append(create_title_page())
    
    # 4. Colofon / Copyright
    print("- Colofonpagina aanmaken...")
    pages.append(create_colophon_page())
    
    # 5. 24 Kleurplaten (enkelzijdig: Kleurplaat rechts, blanco links)
    blank_back = create_blank_back_page()
    for p in pages_data:
        print(f"- Pagina {p['page']}/24: {p['title']}")
        coloring_page = create_coloring_page(p, images_dir)
        pages.append(coloring_page)
        pages.append(blank_back)
        
    # 6. Kleurdiploma
    print("- Kleurdiploma aanmaken...")
    pages.append(create_diploma_page())
    pages.append(blank_page)
    
    # 7. Kleurrijke Achterkant Omslag
    print("- Achterkant toevoegen (in kleur)...")
    back_cover = load_or_create_cover(back_cover_path, is_back=True)
    pages.append(back_cover)
    
    print(f"Totaal aantal pagina's in PDF: {len(pages)}")
    print(f"Opslaan naar {output_pdf}...")
    pages[0].save(
        output_pdf,
        save_all=True,
        append_images=pages[1:],
        resolution=300.0,
        quality=95
    )
    print(f"[OK] Volledig kleurboek PDF klaar: {output_pdf}")

    # Genereer tevens een Amazon KDP Paperback Wrap Cover Spread
    # Rugdikte voor 54 pagina's = ca. 0.122 inch (ca. 37 pixels bij 300 DPI)
    # Totale breedte = Back Cover + Spine + Front Cover + Bleed (0.125 * 2)
    spine_px = 40
    bleed_px = int(0.125 * DPI) # 37 px
    spread_w = PAGE_WIDTH * 2 + spine_px + (bleed_px * 2)
    spread_h = PAGE_HEIGHT + (bleed_px * 2)
    
    spread = Image.new("RGB", (spread_w, spread_h), color=(170, 200, 225))
    
    # Plak achterkant links
    back_resized = back_cover.resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    spread.paste(back_resized, (bleed_px, bleed_px))
    
    # Plak voorkant rechts
    front_resized = front_cover.resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    spread.paste(front_resized, (bleed_px + PAGE_WIDTH + spine_px, bleed_px))
    
    # Rugtekst (Spine)
    draw_spread = ImageDraw.Draw(spread)
    font_spine = get_font(26, bold=True)
    spine_x = bleed_px + PAGE_WIDTH + (spine_px // 2)
    # Lichte ruglijn
    draw_spread.line([(spine_x - spine_px//2, bleed_px), (spine_x - spine_px//2, bleed_px + PAGE_HEIGHT)], fill=(130, 160, 190), width=2)
    draw_spread.line([(spine_x + spine_px//2, bleed_px), (spine_x + spine_px//2, bleed_px + PAGE_HEIGHT)], fill=(130, 160, 190), width=2)

    spread.save(output_cover_spread, resolution=300.0, quality=95)
    print(f"[OK] Paperback Wrap-Around Cover PDF klaar: {output_cover_spread}")

if __name__ == "__main__":
    build_pdf()
