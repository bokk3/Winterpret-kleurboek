import os
import sys
import json
import math
import qrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Constanten voor KDP & Bol.com (8.5 x 8.5 inch bij 300 DPI)
DPI = 300
PAGE_WIDTH = int(8.5 * DPI)   # 2550 pixels
PAGE_HEIGHT = int(8.5 * DPI)  # 2550 pixels
MARGIN = int(0.5 * DPI)       # 150 pixels veiligheidsmarge

DEFAULT_ISBN = "9789403712345"
DEFAULT_BONUS_URL = "https://bas-pip.get.be.eu.org/"
GUTTER_PX = 50 # 50 pixels extra marge aan de rugzijde (rugvouw)

def get_font(size, weight="Medium"):
    """
    Laadt het kindvriendelijke afgeronde Fredoka lettertype (variabele font).
    Valt indien nodig terug op Segoe UI.
    """
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fredoka_path = os.path.join(workspace, "fonts", "Fredoka.ttf")
    
    if os.path.exists(fredoka_path):
        try:
            f = ImageFont.truetype(fredoka_path, size)
            if hasattr(f, "set_variation_by_name"):
                target_weight = "Bold" if weight in ["Bold", "bold"] else "Medium"
                try:
                    f.set_variation_by_name(target_weight)
                except Exception:
                    pass
            return f
        except Exception:
            pass
            
    # Fallback Windows fonts
    font_path = "C:\\Windows\\Fonts\\segoeuib.ttf" if weight in ["Bold", "bold"] else "C:\\Windows\\Fonts\\segoeui.ttf"
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

def draw_star(draw, cx, cy, r_out, r_in, fill=(255, 235, 120), outline=(50, 50, 50), width=4):
    """Tekent een perfecte wiskundige 5-puntige ster als vectorpolygoon."""
    pts = []
    for i in range(10):
        angle = math.pi/2 + i * (math.pi / 5)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    draw.polygon(pts, fill=fill, outline=outline, width=width)

def make_qr_image(url, size_px, fill_color=(25, 45, 75)):
    """Genereert een haarscherpe QR-code voor de bonus landingspagina."""
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=(255, 255, 255)).convert("RGB")
    return img.resize((size_px, size_px), Image.Resampling.LANCZOS)

def generate_and_mount_back_cover_v2_1(back_cover_raw_path, isbn_number, bonus_url, output_path):
    """
    Genereert de geüpdatete achterflap voor Versie 2.1:
    - EAN-13 barcode & Adviesprijs (€ 8,99)
    - Geïntegreerde QR-code badge naar de bonus A4-kleurplaten
    - Fredoka typografie & professionele kinderboekafwerking
    """
    img = Image.open(back_cover_raw_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # 1. Barcode genereren
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
    
    box_w = 955 - 748
    box_h = 940 - 790
    bc_resized = bc_img.resize((box_w, box_h), Image.Resampling.LANCZOS)
    img.paste(bc_resized, (748, 792))
    
    # Prijsvak in Euro's
    draw.rectangle([(748, 942), (955, 974)], fill=(255, 255, 255))
    font_price = get_font(15, weight="Bold")
    draw.text((852, 958), 'Adviesprijs € 8,99', fill=(40, 40, 40), font=font_price, anchor='mm')
    
    # 2. Geïntegreerd informatie- en bonuspaneel met QR-code
    panel_x1 = 125
    panel_y1 = 645
    panel_x2 = 725
    panel_y2 = 885
    draw.rounded_rectangle([(panel_x1, panel_y1), (panel_x2, panel_y2)], radius=24, fill=(255, 255, 255), outline=(140, 170, 200), width=3)
    
    # QR Code links
    qr_img = make_qr_image(bonus_url, 145, fill_color=(25, 45, 75))
    img.paste(qr_img, (145, 665))
    
    f_bold_large = get_font(26, weight="Bold")
    f_bold_med = get_font(20, weight="Bold")
    f_med = get_font(17, weight="Medium")
    f_small_bold = get_font(14, weight="Bold")
    f_small = get_font(13, weight="Medium")
    
    # Tekst onder QR
    draw.text((217, 825), '• GRATIS BONUS •', fill=(215, 95, 25), font=f_small_bold, anchor='mm')
    draw.text((217, 845), '10 Extra A4-Platen!', fill=(30, 45, 65), font=f_small_bold, anchor='mm')
    draw.text((217, 865), 'bas-pip.get.be.eu.org', fill=(100, 120, 140), font=f_small, anchor='mm')
    
    # Scheidslijntje
    draw.line([(305, 665), (305, 865)], fill=(210, 225, 238), width=2)
    
    # Rechterkant tekst
    text_cx = (315 + panel_x2) // 2
    draw.text((text_cx, 680), '24 Vrolijke Winterplaten', fill=(25, 45, 75), font=f_bold_large, anchor='mm')
    draw.text((text_cx, 712), 'OM HEERLIJK IN TE KLEUREN!', fill=(215, 100, 25), font=f_bold_med, anchor='mm')
    
    draw.line([(325, 735), (panel_x2 - 15, 735)], fill=(210, 225, 238), width=2)
    
    draw.text((text_cx, 760), '• Groot formaat & dikke peuterlijnen', fill=(50, 60, 70), font=f_med, anchor='mm')
    draw.text((text_cx, 790), '• Enkelzijdig: stiften drukken niet door!', fill=(50, 60, 70), font=f_med, anchor='mm')
    draw.text((text_cx, 820), '• Incl. Kleurdiploma, Stiftentest & Vriendjes', fill=(50, 60, 70), font=f_med, anchor='mm')
    draw.text((text_cx, 855), 'Voor peuters en kleuters (3 tot 5 jaar)', fill=(110, 130, 150), font=f_med, anchor='mm')
    
    img.save(output_path, quality=95)
    return img

def create_title_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT)
    
    font_title = get_font(130, weight="Bold")
    font_sub = get_font(65, weight="Medium")
    font_tag = get_font(42, weight="Medium")
    
    title_text = "Warme Winterpret"
    sub_text = "met Beertje Bas & Eendje Pip"
    tag_text = "Een knus kleur- en voorleesboek voor peuters & kleuters (3-5 jaar)"
    
    draw.text((PAGE_WIDTH // 2, 750), title_text, fill=(30, 30, 30), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 930), sub_text, fill=(60, 60, 60), font=font_sub, anchor="mm")
    
    draw.line([(PAGE_WIDTH // 2 - 400, 1060), (PAGE_WIDTH // 2 + 400, 1060)], fill=(140, 170, 200), width=6)
    draw.text((PAGE_WIDTH // 2, 1180), tag_text, fill=(80, 80, 80), font=font_tag, anchor="mm")
    
    # Invulkader voor de kleine kunstenaar
    name_box_y = 1650
    draw.rounded_rectangle(
        [(PAGE_WIDTH // 2 - 620, name_box_y), (PAGE_WIDTH // 2 + 620, name_box_y + 330)],
        radius=35, outline=(140, 170, 200), width=5
    )
    font_name = get_font(52, weight="Bold")
    draw.text((PAGE_WIDTH // 2, name_box_y + 80), "Dit vrolijke kleurboek is van:", fill=(40, 60, 80), font=font_name, anchor="mm")
    draw.line([(PAGE_WIDTH // 2 - 450, name_box_y + 225), (PAGE_WIDTH // 2 + 450, name_box_y + 225)], fill=(160, 160, 160), width=3)
    
    return img

def create_colophon_page(isbn_number, bonus_url):
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    font_body = get_font(36, weight="Medium")
    font_bold = get_font(38, weight="Bold")
    
    colophon_lines = [
        ("Warme Winterpret met Beertje Bas & Eendje Pip", True),
        ("Versie 2.1 - Eerste Druk 2026", False),
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
    
    y = 680
    for line, is_bold in colophon_lines:
        font = font_bold if is_bold else font_body
        draw.text((PAGE_WIDTH // 2, y), line, fill=(70, 70, 70) if not is_bold else (30, 30, 30), font=font, anchor="mm")
        y += 62
        
    # QR-code Bonus Box op Colofonpagina
    qr_box_y = 1580
    draw.rounded_rectangle([(PAGE_WIDTH // 2 - 580, qr_box_y), (PAGE_WIDTH // 2 + 580, qr_box_y + 440)], radius=30, fill=(250, 253, 255), outline=(140, 170, 200), width=4)
    
    qr_img = make_qr_image(bonus_url, 300, fill_color=(25, 45, 75))
    img.paste(qr_img, (PAGE_WIDTH // 2 - 510, qr_box_y + 70))
    
    text_x = PAGE_WIDTH // 2 + 80
    draw.text((text_x, qr_box_y + 90), "• GRATIS EXTRA BONUS •", fill=(215, 95, 25), font=get_font(42, weight="Bold"), anchor="mm")
    draw.text((text_x, qr_box_y + 160), "10 Extra A4-Kleurplaten", fill=(25, 45, 75), font=get_font(46, weight="Bold"), anchor="mm")
    draw.text((text_x, qr_box_y + 230), "om thuis af te drukken!", fill=(50, 60, 70), font=get_font(36, weight="Medium"), anchor="mm")
    
    draw.line([(text_x - 220, qr_box_y + 275), (text_x + 220, qr_box_y + 275)], fill=(180, 205, 225), width=2)
    draw.text((text_x, qr_box_y + 330), "Scan de QR-code of surf naar:", fill=(100, 120, 140), font=get_font(28, weight="Medium"), anchor="mm")
    draw.text((text_x, qr_box_y + 375), bonus_url.replace("https://", ""), fill=(25, 45, 75), font=get_font(32, weight="Bold"), anchor="mm")
    
    return img

def create_marker_test_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=100)
    
    font_title = get_font(75, weight="Bold")
    font_sub = get_font(42, weight="Medium")
    font_tag = get_font(36, weight="Bold")
    
    draw.text((PAGE_WIDTH // 2, 350), "•  Test je Kleuren & Stiften  •", fill=(30, 50, 70), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 450), "Probeer hier je lievelingsstiften, potloden en wasco's uit", fill=(70, 70, 70), font=font_sub, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 510), "voordat je aan het grote winterverhaal begint!", fill=(70, 70, 70), font=font_sub, anchor="mm")
    
    colors_info = [
        ("Bas-bruin", "Voor ons beertje", 650, 800),
        ("Pip-geel", "Voor het eendje", 1900, 800),
        ("Mutsjes-rood", "Voor warme mutsen", 650, 1300),
        ("Sneeuw-blauw", "Voor het gladde ijs", 1900, 1300),
        ("Dennengroen", "Voor de kerstbomen", 650, 1800),
        ("Vrije Keuze!", "Jouw lievelingskleur", 1900, 1800),
    ]
    
    for label, desc, cx, cy in colors_info:
        draw.ellipse([(cx - 220, cy - 140), (cx + 220, cy + 140)], outline=(140, 170, 200), width=6, fill=(250, 252, 255))
        draw.ellipse([(cx - 200, cy - 120), (cx + 200, cy + 120)], outline=(200, 220, 235), width=3)
        draw.text((cx, cy - 20), label, fill=(35, 35, 35), font=font_tag, anchor="mm")
        font_desc = get_font(28, weight="Medium")
        draw.text((cx, cy + 35), desc, fill=(120, 120, 120), font=font_desc, anchor="mm")
        
    font_tip = get_font(32, weight="Medium")
    draw.text((PAGE_WIDTH // 2, 2250), "Tip voor mama & papa: Dankzij de enkelzijdige pagina's drukken stiften niet door!", fill=(120, 140, 160), font=font_tip, anchor="mm")
    
    return img

def create_interactive_back_page(page_data, gutter_shift=-GUTTER_PX):
    """
    Interactieve achterkant (Verso / linkerpagina):
    - Gutter-shift naar links (weg van de binnenrug).
    - Unieke op maat gemaakte fantasie-opdracht per scène!
    - Knip-stippellijn aan de buitenkant.
    - 3 Beloningssterretjes om in te kleuren.
    """
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    page_num = page_data["page"]
    title = page_data["title"]
    opdracht = page_data.get("achterkant_opdracht", f"Teken hier jouw eigen idee bij: « {title} »")
    
    # 1. Knip-stippellijn aan de buitenrand (links bij verso)
    cut_x = 180 + gutter_shift
    y = 170
    while y < PAGE_HEIGHT - 150:
        draw.line([(cut_x, y), (cut_x, y + 30)], fill=(160, 175, 190), width=4)
        y += 55
        
    font_cut = get_font(28, weight="Bold")
    draw.text((cut_x + 10, 115), "[ Kniprand om op te hangen ]", fill=(140, 155, 170), font=font_cut, anchor="lm")
    
    # 2. Groot Afgerond Tekenkader
    box_x1 = 300 + gutter_shift
    box_y1 = 160
    box_x2 = PAGE_WIDTH - 150 + gutter_shift
    box_y2 = 2080
    draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], radius=30, outline=(175, 195, 215), width=5)
    
    center_x = (box_x1 + box_x2) // 2
    font_zone_title = get_font(48, weight="Bold")
    draw.text((center_x, box_y1 + 80), "•  Mijn Eigen Winter-Krabbelzone  •", fill=(40, 60, 80), font=font_zone_title, anchor="mm")
    
    font_prompt = get_font(34, weight="Medium")
    draw.text((center_x, box_y1 + 150), opdracht, fill=(90, 115, 140), font=font_prompt, anchor="mm")
    
    # Subtiele sneeuwvlokjes binnenin het vak
    draw_corner_snowflakes(draw, PAGE_WIDTH + (gutter_shift * 2), 2080, margin=260)
    
    # 3. Beloningssterretjes onderaan
    star_cy = 2240
    draw_star(draw, center_x - 130, star_cy, 45, 20)
    draw_star(draw, center_x, star_cy, 45, 20)
    draw_star(draw, center_x + 130, star_cy, 45, 20)
    
    font_stars = get_font(36, weight="Bold")
    draw.text((center_x, star_cy + 85), "Kleur de drie sterretjes in als je kleurplaat klaar is!", fill=(60, 60, 60), font=font_stars, anchor="mm")
    
    return img

def create_coloring_page(page_data, images_dir, gutter_shift=GUTTER_PX):
    """
    Maakt de kleurplaat (Recto / rechterpagina):
    - Gutter-shift naar rechts (weg van de binnenrug).
    - Maximale afbeelding (tot 2000x2000 px).
    - Compact breed tekstvak met voorleestekst én 'Zoekvraagje'!
    """
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    page_num = page_data["page"]
    voorleestekst = page_data["voorleestekst"]
    title = page_data["title"]
    zoek_vraagje = page_data.get("zoek_vraagje", "")
    
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
            
    art_box_y1 = 90
    max_w = 2220
    max_h = 1960
    
    if image_path:
        try:
            art = Image.open(image_path).convert("RGB")
            orig_w, orig_h = art.size
            ratio = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * ratio)
            new_h = int(orig_h * ratio)
            
            art_resized = art.resize((new_w, new_h), Image.Resampling.LANCZOS)
            paste_x = (PAGE_WIDTH - new_w) // 2 + gutter_shift
            paste_y = art_box_y1 + (max_h - new_h) // 2
            
            img.paste(art_resized, (paste_x, paste_y))
            draw.rounded_rectangle([(paste_x, paste_y), (paste_x + new_w, paste_y + new_h)], radius=20, outline=(25, 25, 25), width=5)
            status_text = f"[OK] Pagina {page_num:02d}: Afbeelding geladen"
        except Exception as e:
            status_text = f"[FOUT] Kon {image_path} niet laden: {e}"
    else:
        status_text = f"[PLACEHOLDER] Pagina {page_num:02d}"
        draw.rounded_rectangle([(150 + gutter_shift, art_box_y1), (PAGE_WIDTH - 150 + gutter_shift, art_box_y1 + max_h)], radius=25, outline=(50, 50, 50), width=6)
        font_ph = get_font(65, weight="Bold")
        draw.text((PAGE_WIDTH // 2 + gutter_shift, art_box_y1 + 500), f"Kleurplaat {page_num}: {title}", fill=(60, 60, 60), font=font_ph, anchor="mm")

    # 2. Compact breed voorleesvak onderaan met Zoekvraagje
    tb_x1 = 150 + gutter_shift
    tb_x2 = PAGE_WIDTH - 150 + gutter_shift
    tb_y1 = 2085
    tb_y2 = 2415
    draw.rounded_rectangle([(tb_x1, tb_y1), (tb_x2, tb_y2)], radius=22, outline=(175, 175, 175), width=3)
    
    center_x = (tb_x1 + tb_x2) // 2
    font_story_title = get_font(42, weight="Bold")
    draw.text((center_x, tb_y1 + 45), f"•  {title}  •", fill=(35, 35, 35), font=font_story_title, anchor="mm")
    
    font_story_text = get_font(36, weight="Medium")
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
        
    line_y = tb_y1 + 115
    for line in lines:
        draw.text((center_x, line_y), line, fill=(45, 45, 45), font=font_story_text, anchor="mm")
        line_y += 52
        
    # Zoekvraagje toevoegen
    if zoek_vraagje:
        draw.line([(center_x - 300, tb_y2 - 65), (center_x + 300, tb_y2 - 65)], fill=(220, 225, 230), width=2)
        font_zoek = get_font(30, weight="Bold")
        draw.text((center_x, tb_y2 - 32), f"•  {zoek_vraagje}  •", fill=(210, 95, 25), font=font_zoek, anchor="mm")
        
    font_pg = get_font(34, weight="Medium")
    draw.text((center_x, 2478), f"- {page_num} -", fill=(120, 120, 120), font=font_pg, anchor="mm")
    
    return img, status_text

def create_diploma_page(bonus_url):
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle([(MARGIN + 50, MARGIN + 50), (PAGE_WIDTH - MARGIN - 50, PAGE_HEIGHT - MARGIN - 50)], radius=40, outline=(30, 30, 30), width=10)
    draw.rounded_rectangle([(MARGIN + 75, MARGIN + 75), (PAGE_WIDTH - MARGIN - 75, PAGE_HEIGHT - MARGIN - 75)], radius=35, outline=(150, 150, 150), width=4)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=120)
    
    font_dip_title = get_font(110, weight="Bold")
    font_dip_sub = get_font(50, weight="Medium")
    font_dip_name = get_font(58, weight="Bold")
    
    draw.text((PAGE_WIDTH // 2, 660), "KLEURDIPLOMA", fill=(20, 20, 20), font=font_dip_title, anchor="mm")
    title_w = draw.textlength("KLEURDIPLOMA", font=font_dip_title)
    star_left_x = int((PAGE_WIDTH - title_w) // 2 - 90)
    star_right_x = int((PAGE_WIDTH + title_w) // 2 + 90)
    draw_star(draw, star_left_x, 660, 52, 24, fill=(255, 235, 120), outline=(40, 40, 40), width=5)
    draw_star(draw, star_right_x, 660, 52, 24, fill=(255, 235, 120), outline=(40, 40, 40), width=5)
    
    draw.text((PAGE_WIDTH // 2, 830), "Hoera! Dit officiële winterdiploma is uitgereikt aan:", fill=(70, 70, 70), font=font_dip_sub, anchor="mm")
    
    draw.line([(PAGE_WIDTH // 2 - 600, 1100), (PAGE_WIDTH // 2 + 600, 1100)], fill=(70, 70, 70), width=5)
    draw.text((PAGE_WIDTH // 2, 1050), "( Naam van de kunstenaar )", fill=(160, 160, 160), font=font_dip_sub, anchor="mm")
    
    draw.text((PAGE_WIDTH // 2, 1320), "Omdat jij alle 24 winteravonturen van Beertje Bas & Eendje Pip", fill=(45, 45, 45), font=font_dip_sub, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 1400), "zo prachtig en met zoveel vrolijkheid hebt ingekleurd!", fill=(45, 45, 45), font=font_dip_sub, anchor="mm")
    
    # Handtekeningen en datum
    draw.text((PAGE_WIDTH // 2, 1680), "Liefs van Beertje Bas  &  Eendje Pip", fill=(40, 40, 40), font=font_dip_name, anchor="mm")
    draw.line([(PAGE_WIDTH // 2 - 350, 1910), (PAGE_WIDTH // 2 + 350, 1910)], fill=(180, 180, 180), width=3)
    draw.text((PAGE_WIDTH // 2, 1960), "Datum: ..... / ..... / 202...", fill=(120, 120, 120), font=font_dip_sub, anchor="mm")
    
    # Bonus linkje onderaan diploma
    draw.text((PAGE_WIDTH // 2, 2180), f"Nog niet uitgetekend? Download 10 extra avonturen op {bonus_url.replace('https://', '')}", fill=(110, 130, 150), font=get_font(34, weight="Medium"), anchor="mm")
    
    return img

def create_bonus_activity_page():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_corner_snowflakes(draw, PAGE_WIDTH, PAGE_HEIGHT, margin=100)
    
    font_title = get_font(75, weight="Bold")
    font_sub = get_font(40, weight="Medium")
    
    draw.text((PAGE_WIDTH // 2, 350), "•  BONUS: Winter-Vriendjes om uit te knippen!  •", fill=(30, 50, 70), font=font_title, anchor="mm")
    draw.text((PAGE_WIDTH // 2, 450), "Kleur Bas en Pip in, knip ze voorzichtig uit en speel het verhaal na!", fill=(80, 80, 80), font=font_sub, anchor="mm")
    
    # Bas links
    draw.rounded_rectangle([(250, 600), (1200, 2050)], radius=30, outline=(140, 170, 200), width=5)
    draw.text((725, 700), "Beertje Bas", fill=(40, 40, 40), font=get_font(52, weight="Bold"), anchor="mm")
    draw.text((725, 780), "[ Knip langs de rand ]", fill=(140, 140, 140), font=get_font(32, weight="Medium"), anchor="mm")
    
    # Pip rechts
    draw.rounded_rectangle([(1350, 600), (2300, 2050)], radius=30, outline=(140, 170, 200), width=5)
    draw.text((1825, 700), "Eendje Pip", fill=(40, 40, 40), font=get_font(52, weight="Bold"), anchor="mm")
    draw.text((1825, 780), "[ Knip langs de rand ]", fill=(140, 140, 140), font=get_font(32, weight="Medium"), anchor="mm")
    
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

def build_pdf_v2_1(isbn_number=DEFAULT_ISBN, bonus_url=DEFAULT_BONUS_URL):
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(workspace, "krea_prompts_24_paginas.json")
    images_dir = os.path.join(workspace, "images")
    covers_dir = os.path.join(workspace, "covers")
    
    output_pdf_v2_1 = os.path.join(workspace, "Warme_Winterpret_Kleurboek_v2_1_KDP_Bol.pdf")
    output_pdf_main = os.path.join(workspace, "Warme_Winterpret_Kleurboek_v2_KDP_Bol.pdf")
    output_cover_spread_v2_1 = os.path.join(workspace, "Warme_Winterpret_Cover_Spread_v2_1_KDP.pdf")
    output_cover_spread_main = os.path.join(workspace, "Warme_Winterpret_Cover_Spread_v2_KDP.pdf")
    
    front_cover_path = os.path.join(covers_dir, "front_cover_nl.jpg")
    back_cover_raw_path = os.path.join(covers_dir, "back_cover_nl.jpg")
    back_cover_final_path = os.path.join(covers_dir, "back_cover_v2_barcode.jpg")
    
    # 1. Genereer de officiële achterflap met echte EAN-13 barcode en QR-code bonus
    print(f"1. Achterflap genereren met EAN-13 barcode ({isbn_number}) & QR-code ({bonus_url})...")
    generate_and_mount_back_cover_v2_1(back_cover_raw_path, isbn_number, bonus_url, back_cover_final_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        pages_data = json.load(f)
        
    print("2. Samenstellen van Versie 2.1 (8.5 x 8.5 inch @ 300 DPI - met Gutter Marges & Fredoka)...")
    pages = []
    
    # Omslag Voorkant
    print("- Voorkant toevoegen...")
    front_cover = Image.open(front_cover_path).convert("RGB").resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    pages.append(front_cover)
    
    # Blanco binnenzijde omslag
    blank_white = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color=(255, 255, 255))
    pages.append(blank_white)
    
    # Titelpagina
    print("- Titelpagina aanmaken (Fredoka)...")
    pages.append(create_title_page())
    
    # Colofon met officieel ISBN & QR code
    print("- Colofonpagina aanmaken met QR-code...")
    pages.append(create_colophon_page(isbn_number, bonus_url))
    
    # Stiften & Kleurentest pagina
    print("- Stiften & Kleurentest pagina toevoegen...")
    pages.append(create_marker_test_page())
    pages.append(blank_white)
    
    # 24 Kleurplaten + Unieke Interactieve Achterkanten (met Gutter-marges)
    loaded_count = 0
    for p in pages_data:
        # Kleurplaat (Recto / rechterpagina -> +50px naar rechts)
        coloring_page, status = create_coloring_page(p, images_dir, gutter_shift=GUTTER_PX)
        if "[OK]" in status:
            loaded_count += 1
            print(f"- Pagina {p['page']:02d}/24: {p['title']} [OK] (incl. Zoekvraagje)")
        pages.append(coloring_page)
        
        # Interactieve achterkant (Verso / linkerpagina -> -50px naar links)
        interactive_back = create_interactive_back_page(p, gutter_shift=-GUTTER_PX)
        pages.append(interactive_back)
        
    # Kleurdiploma
    print("- Kleurdiploma aanmaken...")
    pages.append(create_diploma_page(bonus_url))
    pages.append(blank_white)
    
    # Bonus Uitknippagina
    print("- Bonus Uitknip-Vriendjes toevoegen...")
    pages.append(create_bonus_activity_page())
    pages.append(blank_white)
    
    # Omslag Achterkant met echte barcode & QR
    print("- Achterkant toevoegen met EAN-13 barcode & QR bonus...")
    back_cover = Image.open(back_cover_final_path).convert("RGB").resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    pages.append(back_cover)
    
    print(f"Resultaat: Alle {loaded_count} kleurplaten geladen!")
    print(f"Totaal aantal pagina's in Versie 2.1: {len(pages)}")
    print(f"Opslaan naar {output_pdf_v2_1}...")
    pages[0].save(
        output_pdf_v2_1,
        save_all=True,
        append_images=pages[1:],
        resolution=300.0,
        quality=95
    )
    pages[0].save(
        output_pdf_main,
        save_all=True,
        append_images=pages[1:],
        resolution=300.0,
        quality=95
    )
    print(f"[OK] Versie 2.1 PDF klaar: {output_pdf_v2_1}")
    
    # Wrap-around cover spread voor Amazon KDP Paperback & Bol.com
    spine_px = 45
    bleed_px = int(0.125 * DPI) # 37 px
    spread_w = PAGE_WIDTH * 2 + spine_px + (bleed_px * 2)
    spread_h = PAGE_HEIGHT + (bleed_px * 2)
    
    spread = Image.new("RGB", (spread_w, spread_h), color=(225, 240, 250))
    back_cover_resized = back_cover.resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    spread.paste(back_cover_resized, (bleed_px, bleed_px))
    
    front_cover_resized = front_cover.resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    spread.paste(front_cover_resized, (bleed_px + PAGE_WIDTH + spine_px, bleed_px))
    
    draw_spread = ImageDraw.Draw(spread)
    draw_spread.rectangle(
        [(bleed_px + PAGE_WIDTH, bleed_px), (bleed_px + PAGE_WIDTH + spine_px, bleed_px + PAGE_HEIGHT)],
        fill=(135, 175, 205)
    )
    
    spread.save(output_cover_spread_v2_1, resolution=300.0, quality=95)
    spread.save(output_cover_spread_main, resolution=300.0, quality=95)
    print(f"[OK] Versie 2.1 Paperback Cover Spread klaar: {output_cover_spread_v2_1}")

if __name__ == "__main__":
    isbn = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ISBN
    url = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BONUS_URL
    build_pdf_v2_1(isbn, url)
