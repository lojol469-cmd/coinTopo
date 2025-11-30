from PIL import Image, ImageDraw, ImageFont
import os

def create_topocoin_logo():
    # Dimensions du logo
    width, height = 400, 400

    # Créer une image avec fond dégradé bleu
    img = Image.new('RGB', (width, height), color='#1e3a8a')
    draw = ImageDraw.Draw(img)

    # Dégradé simple
    for y in range(height):
        r = int(30 + (100 - 30) * (y / height))
        g = int(58 + (150 - 58) * (y / height))
        b = int(138 + (200 - 138) * (y / height))
        for x in range(width):
            draw.point((x, y), fill=(r, g, b))

    # Cercle central
    center = (width // 2, height // 2)
    radius = 150
    draw.ellipse(
        [(center[0] - radius, center[1] - radius),
         (center[0] + radius, center[1] + radius)],
        fill='#fbbf24',
        outline='#f59e0b',
        width=5
    )

    # Lettres TPC stylisées
    try:
        # Essayer une police système
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        # Police par défaut
        font = ImageFont.load_default()

    # Texte TPC
    text = "TPC"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    draw.text((text_x, text_y), text, fill='#1e3a8a', font=font)

    # Texte Topocoin en dessous
    try:
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        small_font = ImageFont.load_default()

    subtitle = "Topocoin"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=small_font)
    sub_width = bbox_sub[2] - bbox_sub[0]
    sub_x = (width - sub_width) // 2
    sub_y = text_y + text_height + 20

    draw.text((sub_x, sub_y), subtitle, fill='#fbbf24', font=small_font)

    # Sauvegarder
    img.save('topocoin_logo.png')
    print("Logo créé : topocoin_logo.png")

if __name__ == "__main__":
    create_topocoin_logo()