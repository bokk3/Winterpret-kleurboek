import os
import json
import math
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Constanten voor KDP & Bol.com (8.5 x 8.5 inch bij 300 DPI)
DPI = 300
PAGE_WIDTH = int(8.5 * DPI)   # 2550 pixels
PAGE_HEIGHT = int(8.5 * DPI)  # 2550 pixels
MARGIN = int(0.5 * DPI)       # 150 pixels veiligheidsmarge

DEFAULT_ISBN = "9789403712345" # Standaard voorbeeld-ISBN (vervangbaar via argument)

def get_font(size, bold=False):
    """Laadt professionele Windows systeemfonts (Segoe UI) met schone typografie."""
    font_path = "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_corner_snowflakes(draw, width, height, margin=80):
    """Tekent subtiele decoratieve sneeuwvlokjes in de hoeken."""
    def snowflake(x, y, r=25):
        draw.line([(x - r, y), (x + r, y)], fill=(190, 205, 220), width=4)
        draw.line([(x, y - r), (x, y + r)], fill=(190, 205, 220), width=4)
        draw.line([(x - r*0.7, y - r*0.7), (x + r*0.7, y + r*0.7)], fill=(190, 205, 220), width=3)
        draw.line([(x - r*0.7, y + r*0.7), (x + r*0.7, y - r*0.7)], fill=(190, 205, 220), width=3)

    snowflake(margin + 50, margin + 50)
    snowflake(width - margin - 50, margin + 50)
    snowflake(margin + 50, height - margin - 50)
    snowflake(width - margin - 50, height - margin - 50)

def draw_star(draw, cx, cy, r_out, r_in, fill=(255, 255, 255), outline=(60, 60, 60), width=4):
    """Tekent een perfecte wiskundige 5-puntige ster als vectorpolygoon."""
    pts = []
    for i in range(10):
        angle = math.pi/2 + i * (math.pi / 5)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    draw.polygon(pts, fill=fill, outline=outline, width=width)

def generate_and_mount_barcode(back_cover_raw_path, isbn_number, output_path):
    """Genereert een officiële EAN-13 barcode en monteert deze op de achterkant."""
    img = Image.open(back_cover_raw_path).convert("RGB")
    
    # 1. Genereer barcode via python-barcode
    isbn_class = barcode.get_barcode_class('isbn13')
    writer = ImageWriter()
    writer.set_options({
        'module_width': 0.35,
        'module_height': 14.0,
        'font_size': 10,
        'text_distance': 4.0,
        'quiet_zone': 2.0
    })
    bc = isbn_class(isbn_number, writer=writer)
    bc_img = bc.render()
    
    # Afmeting barcodevak op achterflap (1024x1024 basis)
    box_w = 955 - 748
    box_h = 940 - 790
    bc_resized = bc_img.resize((box_w, box_h), Image.Resampling.LANCZOS)
    img.paste(bc_resized, (748, 792))
    
    # Prijsvak in Euro's
    draw = ImageDraw.Draw(img)
    draw.rectangle([(748, 942), (955, 974)], fill=(255, 255, 255))
    font_price = get_font(16, bold=True)
    draw.text((852, 958), 'Adviesprijs € 8,99', fill=(40, 40, 40), font=font_price, anchor='mm')
    
    img.save(output_path, quality=95)
    return img

def create_title_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT)
    
    font_title = get_font(130, bold=True)
    font_sub = get_font(65, bold=False)
    font_tag = get_font(44, bold=True)
    
    title_text = "Warme Winterpret"
    sub_text = "met Beertje Bas & Eendje Pip"
    tag_text = "Een knus kleur- en voorleesboek voor peuters & kleuters (3-5 jaar)"
    
    draw.text((PAGE_WIDTH // 2, 750), title_text, fill=(30, 30, 30), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 930), sub_text, fill=(60, 60, 60), font=font_sub, anchor="mm")
    
    draw.line([(PAGE_WIDTH // 2 - 400, 1060), (PAGE_WIDTH // 2 + 400, 1060)], fill=(140, 170, 200), width=6)
    draw.text((PAGE_WIDTH // 2, 1180), tag_text, fill=(75, 75, 75), font=font_tag, anchor="mm")
    
    # Invulkader voor de kleine kunstenaar
    name_box_y = 1650
    draw.rounded_rectangle(
        [(PAGE_WIDTH // 2 - 600, name_box_y), (PAGE_WIDTH // 2 + 600, name_box_y + 320)],
        radius=30, outline=(140, 170, 200), width=5
    )
    font_name = get_font(52, bold=False)
    draw.text((PAGE_WIDTH // 2, name_box_y + 80), "Dit vrolijke kleurboek is van:", fill=(65, 65, 65), font=font_name, anchor="mm")
    draw.line([(PAGE_WIDTH // 2 - 450, name_box_y + 220), (PAGE_WIDTH // 2 + 450, name_box_y + 220)], fill=(160, 160, 160), width=3)
    
    return img

def create_colophon_page(isbn_number):
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_body = get_font(36, bold=False)
    font_bold = get_font(38, bold=True)
    
    colophon_lines = [
        ("Warme Winterpret met Beertje Bas & Eendje Pip", True),
        ("Versie 2.0 - Eerste Druk 2026", False),
        ("", False),
        ("Tekst & Illustratieconcept: Eigen Uitgave", False),
        ("Vlaams Nederlands - Doelgroep 3 tot 5 jaar", False),
        ("NUR 228 (Prenten- & Kleurboeken)", False),
        (f"ISBN: {isbn_number}", True),
        ("", False),
        ("Alle rechten voorbehouden.", False),
        ("Niets uit deze uitgave mag worden verveelvoudigd zonder voorafgaande toestemming.", False),
        ("", False),
        ("Gedrukt op milieuvriendelijk papier via Print-on-Demand.", False)
    ]
    
    y = 1000
    for line, is_bold in colophon_lines:
        font = font_bold if is_bold else font_body
        draw.text((PAGE_WIDTH // 2, y), line, fill=(70, 70, 70) if not is_bold else (30, 30, 30), font=font, anchor="mm")
        y += 65
        
    return img

def create_marker_test_page():
    """Nieuw in Versie 2.0: De Stiften & Kleurentest pagina."""
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=100)
    
    font_title = get_font(75, bold=True)
    font_sub = get_font(42, bold=False)
    font_tag = get_font(36, bold=True)
    
    draw.text((PAGE_WIDTH // 2, 350), "•  Test je Kleuren & Stiften  •", fill=(30, 50, 70), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 450), "Probeer hier je lievelingsstiften, potloden en wasco's uit", fill=(80, 80, 80), font=font_sub, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 510), "voordat je aan het grote winterverhaal begint!", fill=(80, 80, 80), font=font_sub, anchor="mm")
    
    # 6 Grote Kleur-Testpotjes / Cirkels
    colors_info = [
        ("Bas-bruin", "Voor ons beertje", 650, 800),
        ("Pip-geel", "Voor het eendje", 1900, 800),
        ("Mutsjes-rood", "Voor warme mutsen", 650, 1300),
        ("Sneeuw-blauw", "Voor het gladde ijs", 1900, 1300),
        ("Dennengroen", "Voor de kerstbomen", 650, 1800),
        ("Vrije Keuze!", "Jouw lievelingskleur", 1900, 1800),
    ]
    
    for label, desc, cx, cy in colors_info:
        # Teken een grote vriendelijke afgeronde testcirkel
        draw.ellipse([(cx - 220, cy - 140), (cx + 220, cy + 140)], outline=(140, 170, 200), width=6, fill=(250, 252, 255))
        # Binnenste stippellijntje
        draw.ellipse([(cx - 200, cy - 120), (cx + 200, cy + 120)], outline=(200, 220, 235), width=3)
        draw.text((cx, cy - 20), label, fill=(35, 35, 35), font=font_tag, anchor="mm")
        font_desc = get_font(28, bold=False)
        draw.text((cx, cy + 35), desc, fill=(120, 120, 120), font=font_desc, anchor="mm")
        
    font_tip = get_font(32, bold=False)
    draw.text((PAGE_WIDTH // 2, 2250), "Tip voor mama & papa: Dankzij de enkelzijdige pagina's drukken stiften niet door!", fill=(130, 150, 170), font=font_tip, anchor="mm")
    
    return img

def create_interactive_back_page(page_num, title):
    """Nieuw in Versie 2.0: Interactieve Krabbelzone + Kniprand + Beloningssterretjes."""
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Knip-stippellijn aan de linker marge
    cut_x = 180
    y = 170
    while y < PAGE_HEIGHT - 150:
        draw.line([(cut_x, y), (cut_x, y + 30)], fill=(160, 175, 190), width=4)
        y += 55
        
    font_cut = get_font(28, bold=True)
    draw.text((cut_x + 10, 115), "[ Kniprand om op te hangen ]", fill=(140, 155, 170), font=font_cut, anchor="lm")
    
    # 2. Groot Afgerond Tekenkader
    box_x1 = 300
    box_y1 = 160
    box_x2 = PAGE_WIDTH - 150
    box_y2 = 2080
    draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=30, outline=(175, 195, 215), width=5)
    
    font_zone_title = get_font(48, bold=True)
    draw.text(((box_x1 + box_x2)//2, box_y1 + 80), "•  Mijn Eigen Winter-Krabbelzone  •", fill=(40, 60, 80), font=font_zone_title, anchor="mm")
    
    font_prompt = get_font(34, bold=False)
    draw.text(((box_x1 + box_x2)//2, box_y1 + 150), f"Teken hier jouw eigen idee bij: « {title} »", fill=(110, 130, 150), font=font_prompt, anchor="mm")
    
    # Subtiele sneeuwvlokjes binnenin het vak
    draw_corner_snowflakes(draw, PAGE_WIDTH, 2080, margin=260)
    
    # 3. Beloningssterretjes onderaan
    star_cy = 2240
    star_cx = (box_x1 + box_x2) // 2
    draw_star(draw, star_cx - 130, star_cy, 45, 20)
    draw_star(draw, star_cx, star_cy, 45, 20)
    draw_star(draw, star_cx + 130, star_cy, 45, 20)
    
    font_stars = get_font(36, bold=True)
    draw.text((star_cx, star_cy + 85), "Kleur de drie sterretjes in als je kleurplaat klaar is!", fill=(60, 60, 60), font=font_stars, anchor="mm")
    
    return img

def create_coloring_page(page_data, images_dir):
    """Maakt de kleurplaat met royale afbeelding (2000x2000) en compact breed tekstvak."""
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    page_num = page_data["page"]
    voorleestekst = page_data["voorleestekst"]
    title = page_data["title"]
    
    # Zoek afbeelding
    candidates = [
        f"pagina_{page_num:02d}.png",
        f"Pagina_{page_num:02d}.png",
        f"pagina_{page_num}.png",
        f"Pagina_{page_num}.png",
    ]
    image_path = None
    for c in candidates:
        p = os.path.join(images_dir, c)
        if os.path.exists(p):
            image_path = p
            break
            
    art_box_y1 = 95
    max_w = 2250
    max_h = 2000
    
    if image_path:
        try:
            art = Image.open(image_path).convert("RGB")
            orig_w, orig_h = art.size
            ratio = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * ratio)
            new_h = int(orig_h * ratio)
            
            art_resized = art.resize((new_w, new_h), Image.Resampling.LANCZOS)
            paste_x = (PAGE_WIDTH - new_w) // 2
            paste_y = art_box_y1 + (max_h - new_h) // 2
            
            img.paste(art_resized, (paste_x, paste_y))
            draw.rounded_rectangle([(paste_x, paste_y), (paste_x + new_w, paste_y + new_h)], radius=20, outline=(25, 25, 25), width=5)
            status_text = f"[OK] Pagina {page_num:02d}: Afbeelding geladen"
        except Exception as e:
            status_text = f"[FOUT] Kon {image_path} niet laden: {e}"
    else:
        status_text = f"[PLACEHOLDER] Pagina {page_num:02d}"
        draw.rounded_rectangle([(150, art_box_y1), (PAGE_WIDTH - 150, art_box_y1 + max_h)], radius=25, outline=(50, 50, 50), width=6)
        font_ph = get_font(65, bold=True)
        draw.text((PAGE_WIDTH // 2, art_box_y1 + 500), f"Kleurplaat {page_num}: {title}", fill=(60, 60, 60), font=font_ph, anchor="mm")

    # 2. Compact breed voorleesvak onderaan
    tb_x1 = 150
    tb_x2 = PAGE_WIDTH - 150
    tb_y1 = 2125
    tb_y2 = 2415
    draw.rounded_rectangle([(tb_x1, tb_y1), (tb_x2, tb_y2)], radius=22, outline=(175, 175, 175), width=3)
    
    font_story_title = get_font(44, bold=True)
    draw.text((PAGE_WIDTH // 2, tb_y1 + 52), f"•  {title}  •", fill=(35, 35, 35), font=font_story_title, anchor="mm")
    
    font_story_text = get_font(38, bold=False)
    words = voorleestekst.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if len(test_line) > 78:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(" ".join(current_line))
        
    line_y = tb_y1 + 130
    for line in lines:
        draw.text((PAGE_WIDTH // 2, line_y), line, fill=(45, 45, 45), font=font_story_text, anchor="mm")
        line_y += 56
        
    font_pg = get_font(34, bold=False)
    draw.text((PAGE_WIDTH // 2, 2478), f"- {page_num} -", fill=(120, 120, 120), font=font_pg, anchor="mm")
    
    return img, status_text

def create_diploma_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle([(MARGIN + 50, MARGIN + 50), (PAGE_WIDTH - MARGIN - 50, PAGE_HEIGHT - MARGIN - 50)], radius=40, outline=(30, 30, 30), width=10)
    draw.rounded_rectangle([(MARGIN + 75, MARGIN + 75), (PAGE_WIDTH - MARGIN - 75, PAGE_HEIGHT - MARGIN - 75)], radius=35, outline=(150, 150, 150), width=4)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=120)
    
    font_dip_title = get_font(110, bold=True)
    font_dip_sub = get_font(52, bold=False)
    font_dip_name = get_font(60, bold=True)
    
    draw.text((PAGE_WIDTH // 2, 680), "KLEURDIPLOMA", fill=(20, 20, 20), font=font_dip_title, anchor="mm")
    title_w = draw.textlength("KLEURDIPLOMA", font=font_dip_title)
    star_left_x = int((PAGE_WIDTH - title_w) // 2 - 90)
    star_right_x = int((PAGE_WIDTH + title_w) // 2 + 90)
    draw_star(draw, star_left_x, 680, 52, 24, fill=(255, 235, 120), outline=(40, 40, 40), width=5)
    draw_star(draw, star_right_x, 680, 52, 24, fill=(255, 235, 120), outline=(40, 40, 40), width=5)
    
    draw.text((PAGE_WIDTH // 2, 850), "Hoera! Dit officiële winterdiploma is uitgereikt aan:", fill=(70, 70, 70), font=font_dip_sub, anchor="mm")
    
    draw.line([(PAGE_WIDTH // 2 - 600, 1120), (PAGE_WIDTH // 2 + 600, 1120)], fill=(70, 70, 70), width=5)
    draw.text((PAGE_WIDTH // 2, 1070), "( Naam van de kunstenaar )", fill=(160, 160, 160), font=font_dip_sub, anchor="mm")
    
    draw.text((PAGE_WIDTH // 2, 1340), "Omdat jij alle 24 winteravonturen van Beertje Bas & Eendje Pip", fill=(45, 45, 45), font=font_dip_sub, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 1420), "zo prachtig en met zoveel vrolijkheid hebt ingekleurd!", fill=(45, 45, 45), font=font_dip_sub, anchor="mm")
    
    # Handtekeningen en datum
    draw.text((PAGE_WIDTH // 2, 1720), "Liefs van Beertje Bas  &  Eendje Pip", fill=(40, 40, 40), font=font_dip_name, anchor="mm")
    draw.line([(PAGE_WIDTH // 2 - 350, 1950), (PAGE_WIDTH // 2 + 350, 1950)], fill=(180, 180, 180), width=3)
    draw.text((PAGE_WIDTH // 2, 2000), "Datum: ..... / ..... / 202...", fill=(120, 120, 120), font=font_dip_sub, anchor="mm")
    
    return img

def create_bonus_activity_page():
    """Nieuw in Versie 2.0: Bonus Uitknip-Vriendjes Pagina."""
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=100)
    
    font_title = get_font(75, bold=True)
    font_sub = get_font(40, bold=False)
    
    draw.text((PAGE_WIDTH // 2, 350), "•  BONUS: Winter-Vriendjes om uit te knippen!  •", fill=(30, 50, 70), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 450), "Kleur Bas en Pip in, knip ze voorzichtig uit en speel het verhaal na!", fill=(80, 80, 80), font=font_sub, anchor="mm")
    
    # Twee grote uitknipkaders met stippellijntjes
    # Bas links
    draw.rounded_rectangle([(250, 600), (1200, 2050)], radius=30, outline=(140, 170, 200), width=5)
    draw.text((725, 700), "Beertje Bas", fill=(40, 40, 40), font=get_font(52, bold=True), anchor="mm")
    draw.text((725, 780), "[ Knip langs de rand ]", fill=(140, 140, 140), font=get_font(32, bold=False), anchor="mm")
    
    # Pip rechts
    draw.rounded_rectangle([(1350, 600), (2300, 2050)], radius=30, outline=(140, 170, 200), width=5)
    draw.text((1825, 700), "Eendje Pip", fill=(40, 40, 40), font=get_font(52, bold=True), anchor="mm")
    draw.text((1825, 780), "[ Knip langs de rand ]", fill=(140, 140, 140), font=get_font(32, bold=False), anchor="mm")
    
    # Plak echte Bas (pagina 2) en echte Pip (pagina 5)
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(workspace, "images")
    
    p2_path = os.path.join(images_dir, "Pagina_02.png")
    p5_path = os.path.join(images_dir, "Pagina_05.png")
    
    if os.path.exists(p2_path):
        p_bas = Image.open(p2_path).convert("RGB").crop((70, 80, 580, 780)).resize((720, 1000), Image.Resampling.LANCZOS)
        img.paste(p_bas, (365, 900))
    elif os.path.exists(os.path.join(images_dir, "Pagina_01.png")):
        p_bas = Image.open(os.path.join(images_dir, "Pagina_01.png")).convert("RGB").crop((150, 200, 550, 900)).resize((720, 1000), Image.Resampling.LANCZOS)
        img.paste(p_bas, (365, 900))
        
    if os.path.exists(p5_path):
        p_pip = Image.open(p5_path).convert("RGB").crop((30, 120, 520, 720)).resize((720, 1000), Image.Resampling.LANCZOS)
        img.paste(p_pip, (1465, 900))
        
    return img

def build_pdf_v2(isbn_number=DEFAULT_ISBN):
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(workspace, "krea_prompts_24_paginas.json")
    images_dir = os.path.join(workspace, "images")
    covers_dir = os.path.join(workspace, "covers")
    
    output_pdf = os.path.join(workspace, "Warme_Winterpret_Kleurboek_v2_KDP_Bol.pdf")
    output_cover_spread = os.path.join(workspace, "Warme_Winterpret_Cover_Spread_v2_KDP.pdf")
    
    front_cover_path = os.path.join(covers_dir, "front_cover_nl.jpg")
    back_cover_raw_path = os.path.join(covers_dir, "back_cover_nl.jpg")
    back_cover_final_path = os.path.join(covers_dir, "back_cover_v2_barcode.jpg")
    
    # Genereer de officiële achterflap met echte EAN-13 barcode en Euro prijs
    print(f"1. Officiële EAN-13 barcode genereren voor ISBN: {isbn_number}...")
    generate_and_mount_barcode(back_cover_raw_path, isbn_number, back_cover_final_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        pages_data = json.load(f)
        
    print("2. Samenstellen van Versie 2.0 (8.5 x 8.5 inch @ 300 DPI)...")
    pages = []
    
    # Omslag Voorkant
    print("- Voorkant toevoegen...")
    front_cover = Image.open(front_cover_path).convert("RGB").resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    pages.append(front_cover)
    
    # Blanco binnenzijde omslag
    blank_white = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    pages.append(blank_white)
    
    # Titelpagina
    print("- Titelpagina aanmaken...")
    pages.append(create_title_page())
    
    # Colofon met officieel ISBN
    print("- Colofonpagina aanmaken...")
    pages.append(create_colophon_page(isbn_number))
    
    # Stiften & Kleurentest pagina
    print("- Stiften & Kleurentest pagina toevoegen...")
    pages.append(create_marker_test_page())
    pages.append(blank_white)
    
    # 24 Kleurplaten + Interactieve Achterkanten
    loaded_count = 0
    for p in pages_data:
        coloring_page, status = create_coloring_page(p, images_dir)
        if "[OK]" in status:
            loaded_count += 1
            print(f"- Pagina {p['page']:02d}/24: {p['title']} [OK]")
        pages.append(coloring_page)
        
        # Interactieve achterkant (Krabbelzone + Beloningssterretjes + Kniprand)
        interactive_back = create_interactive_back_page(p['page'], p['title'])
        pages.append(interactive_back)
        
    # Kleurdiploma
    print("- Kleurdiploma aanmaken...")
    pages.append(create_diploma_page())
    pages.append(blank_white)
    
    # Bonus Uitknippagina
    print("- Bonus Uitknip-Vriendjes toevoegen...")
    pages.append(create_bonus_activity_page())
    pages.append(blank_white)
    
    # Omslag Achterkant met echte barcode
    print("- Achterkant toevoegen met EAN-13 barcode...")
    back_cover = Image.open(back_cover_final_path).convert("RGB").resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    pages.append(back_cover)
    
    print(f"Resultaat: Alle {loaded_count} kleurplaten geladen!")
    print(f"Totaal aantal pagina's in Versie 2.0: {len(pages)}")
    print(f"Opslaan naar {output_pdf}...")
    pages[0].save(
        output_pdf,
        save_all=True,
        append_images=pages[1:],
        resolution=300.0,
        quality=95
    )
    print(f"[OK] Versie 2.0 PDF klaar: {output_pdf}")
    
    # Wrap-around cover spread voor Amazon KDP Paperback & Bol.com
    # Rugdikte voor ca. 60 pagina's = ca. 45 px bij 300 DPI
    spine_px = 45
    bleed_px = int(0.125 * DPI) # 37 px
    spread_w = PAGE_WIDTH * 2 + spine_px + (bleed_px * 2)
    spread_h = PAGE_HEIGHT + (bleed_px * 2)
    
    spread = Image.new("RGB", (spread_w, spread_h), color=(170, 200, 225))
    spread.paste(back_cover, (bleed_px, bleed_px))
    spread.paste(front_cover, (bleed_px + PAGE_WIDTH + spine_px, bleed_px))
    
    draw_spread = ImageDraw.Draw(spread)
    spine_x = bleed_px + PAGE_WIDTH + (spine_px // 2)
    draw_spread.line([(spine_x - spine_px//2, bleed_px), (spine_x - spine_px//2, bleed_px + PAGE_HEIGHT)], fill=(130, 160, 190), width=2)
    draw_spread.line([(spine_x + spine_px//2, bleed_px), (spine_x + spine_px//2, bleed_px + PAGE_HEIGHT)], fill=(130, 160, 190), width=2)
    
    spread.save(output_cover_spread, resolution=300.0, quality=95)
    print(f"[OK] Versie 2.0 Paperback Cover Spread klaar: {output_cover_spread}")

if __name__ == "__main__":
    build_pdf_v2()
