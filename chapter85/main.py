import os
from PIL import Image, ImageDraw, ImageFont


def add_watermark_overlay(input_image_path, output_image_path, watermark_text):
    image_input = Image.open(input_image_path)
    image_input = image_input.convert('RGBA')
    width, heigth = image_input.size

    overlay_img = Image.new(size=image_input.size, mode='RGBA', color=(255,255,255,0))

    draw = ImageDraw.Draw(overlay_img)

    watermark_color_pattern = (255,255,255,30)

    for i in range(0, width + heigth, 50):
        draw.line([(0, heigth-i), (i, heigth)], fill=watermark_color_pattern, width=5)

    font_size = 80
    font = ImageFont.truetype(size=font_size, font="arial.ttf")


    text_width, text_height = draw.textsize(watermark_text, font)

    x = (width - text_width) // 2
    y = (heigth - text_height) //2

    watermark_color_text = (255,255,255, 80)
    draw.text((x, y), watermark_text, fill=watermark_color_text, font=font)
    watermark_image = Image.alpha_composite(image_input, overlay_img)

    watermark_image.save(output_image_path)


input_image_path = 'input_image.jpg'
output_image_path = 'output_image.png'
watermark_text = "Copywrite"

# add_watermark_overlay(input_image_path, output_image_path, watermark_text)

for file in os.listdir('images'):
    add_watermark_overlay(input_image_path=f"images/{file}", output_image_path=f"images/watermarked_{file.replace('jpg', 'png')}", watermark_text = "Copywrite")