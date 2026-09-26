import os
from PIL import Image, ImageDraw, ImageFont

root_dir = r"C:\Codes\Day9-Road-Elements-Lab-Student"
gts_dir = os.path.join(root_dir, "guideline-challenge", "data", "gtsdb")
assets_dir = os.path.join(root_dir, "slide_assets")
challenge_assets_dir = os.path.join(root_dir, "guideline-challenge", "slide_assets")

os.makedirs(assets_dir, exist_ok=True)
os.makedirs(challenge_assets_dir, exist_ok=True)

def get_font(size, bold=False):
    font_path = "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

font_label = get_font(13, bold=True)
font_small = get_font(11, bold=False)

def save_both(img, name):
    img.save(os.path.join(assets_dir, name))
    img.save(os.path.join(challenge_assets_dir, name))
    print(f"Saved {name}")

# 1. Slide 2: GTS04 Truck vs 120 (Phantom braking proof)
img_gts04 = Image.open(os.path.join(gts_dir, "GTS04.png"))
crop_04 = img_gts04.crop((920, 425, 1020, 515))
crop_04 = crop_04.resize((320, 280), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(crop_04)
b120 = [120, 52, 195, 125]
draw.rectangle(b120, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([b120[1] - 40, b120[1] - 38, b120[1] + 95, b120[1] - 16], radius=3, fill=(43, 182, 115))
draw.text((b120[1] - 36, b120[1] - 36), "120 · RELEVANT", font=font_label, fill=(255, 255, 255))
btruck = [120, 125, 195, 198]
draw.rectangle(btruck, outline=(245, 158, 11), width=3)
draw.rounded_rectangle([btruck[1] - 40, btruck[3] + 4, btruck[1] + 105, btruck[3] + 24], radius=3, fill=(245, 158, 11))
draw.text((btruck[1] - 36, btruck[3] + 6), "XE TẢI · NOT_REL", font=font_label, fill=(26, 22, 0))
draw.rectangle([0, crop_04.height - 24, crop_04.width, crop_04.height], fill=(16, 18, 16))
draw.text((8, crop_04.height - 20), "GTS04: Xe con tuân thủ 120, cấm xe tải là NOT_RELEVANT", font=font_small, fill=(240, 196, 0))
save_both(crop_04, "evidence_gts04_truck.png")

# 2. Slide 3: GTS09 (Scope: Ignore square vs Label round keep right)
img_gts09 = Image.open(os.path.join(gts_dir, "GTS09.png"))
crop_09 = img_gts09.crop((350, 420, 470, 665))
crop_09 = crop_09.resize((240, 460), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(crop_09)
sq_box = [45, 60, 195, 205]
draw.rectangle(sq_box, outline=(226, 59, 47), width=3)
draw.rounded_rectangle([15, 34, 225, 56], radius=3, fill=(226, 59, 47))
draw.text((22, 37), "IGNORE: Biển vuông ngoài 43 class", font=font_small, fill=(255, 255, 255))
kr_box = [75, 350, 165, 440]
draw.rectangle(kr_box, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([20, 324, 220, 346], radius=3, fill=(43, 182, 115))
draw.text((28, 327), "LABEL: 38 keep right (RELEVANT)", font=font_small, fill=(255, 255, 255))
draw.rectangle([0, crop_09.height - 24, crop_09.width, crop_09.height], fill=(16, 18, 16))
draw.text((8, crop_09.height - 20), "GTS09: Biển vuông = IGNORE · Biển tròn = LABEL", font=font_small, fill=(240, 196, 0))
save_both(crop_09, "evidence_gts09_scope.png")

# 3. Slide 5: GTS01 (Geometry: 3 independent tight boxes on pole)
img_gts01 = Image.open(os.path.join(gts_dir, "GTS01.png"))
crop_01 = img_gts01.crop((715, 400, 765, 530))
crop_01 = crop_01.resize((200, 460), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(crop_01)
# Scale: 4x x, 3.54x y
# Triangle: y=68..170, x=15..185
b_tri = [15, 70, 185, 172]
draw.rectangle(b_tri, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([15, 45, 185, 67], radius=3, fill=(43, 182, 115))
draw.text((25, 48), "Box 1: Trơn trượt", font=font_small, fill=(255, 255, 255))

# Speed 50: y=174..260, x=28..172
b_50 = [28, 174, 172, 260]
draw.rectangle(b_50, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([28, 264, 172, 284], radius=3, fill=(43, 182, 115))
draw.text((40, 266), "Box 2: Tốc độ 50", font=font_small, fill=(255, 255, 255))

# No overtaking: y=288..376, x=30..170
b_over = [30, 288, 170, 376]
draw.rectangle(b_over, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([30, 380, 170, 400], radius=3, fill=(43, 182, 115))
draw.text((42, 382), "Box 3: Cấm vượt", font=font_small, fill=(255, 255, 255))

# Red X on pole
draw.line([85, 408, 115, 432], fill=(226, 59, 47), width=3)
draw.line([115, 408, 85, 432], fill=(226, 59, 47), width=3)
draw.text((25, 434), "KHÔNG lấy cột đỡ", font=font_small, fill=(226, 59, 47))

draw.rectangle([0, crop_01.height - 24, crop_01.width, crop_01.height], fill=(16, 18, 16))
draw.text((8, crop_01.height - 20), "GTS01: 3 box độc lập (≤ 3px)", font=font_small, fill=(240, 196, 0))
save_both(crop_01, "evidence_gts01_stacked.png")

# 4. Slide 6: GTS10 Spatial Relevance (2 signs same class)
img_gts10 = Image.open(os.path.join(gts_dir, "GTS10.png"))
comp_gts10 = img_gts10.resize((680, 360), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(comp_gts10)
bx_left = [100, 182, 124, 203]
draw.rectangle(bx_left, outline=(245, 158, 11), width=3)
draw.rounded_rectangle([bx_left[0] - 25, bx_left[1] - 24, bx_left[0] + 95, bx_left[1] - 2], radius=3, fill=(245, 158, 11))
draw.text((bx_left[0] - 20, bx_left[1] - 22), "Góc xa · NOT_REL", font=font_small, fill=(26, 22, 0))

bx_right = [594, 152, 622, 175]
draw.rectangle(bx_right, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([bx_right[0] - 70, bx_right[1] - 24, bx_right[0] + 45, bx_right[1] - 2], radius=3, fill=(43, 182, 115))
draw.text((bx_right[0] - 65, bx_right[1] - 22), "Lối rẽ ego · RELEVANT", font=font_small, fill=(255, 255, 255))

bx_p = [293, 238, 307, 252]
draw.rectangle(bx_p, outline=(226, 59, 47), width=2)
draw.text((bx_p[0] - 18, bx_p[3] + 2), "P · IGNORE", font=font_small, fill=(226, 59, 47))

draw.rectangle([0, comp_gts10.height - 26, comp_gts10.width, comp_gts10.height], fill=(16, 18, 16))
draw.text((12, comp_gts10.height - 21), "GTS10: Cùng class 33 go right — Relevance phụ thuộc vị trí tương quan với làn ego!", font=font_label, fill=(240, 196, 0))
save_both(comp_gts10, "evidence_gts10_spatial.png")

# 5. Slide 6/7: GTS03 Pedestrian Crossing & Speed 20
img_gts03 = Image.open(os.path.join(gts_dir, "GTS03.png"))
crop_03 = img_gts03.crop((1070, 425, 1175, 520))
crop_03 = crop_03.resize((320, 280), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(crop_03)
b_ped = [134, 38, 250, 135]
draw.rectangle(b_ped, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([10, 36, 126, 58], radius=3, fill=(43, 182, 115))
draw.text((16, 40), "27 Người đi bộ", font=font_small, fill=(255, 255, 255))

b_sp20 = [143, 144, 230, 224]
draw.rectangle(b_sp20, outline=(43, 182, 115), width=3)
draw.rounded_rectangle([10, 144, 135, 166], radius=3, fill=(43, 182, 115))
draw.text((16, 148), "00 Tốc độ 20", font=font_small, fill=(255, 255, 255))

draw.rectangle([0, crop_03.height - 24, crop_03.width, crop_03.height], fill=(16, 18, 16))
draw.text((8, crop_03.height - 20), "GTS03: Biển ngã tư = RELEVANT (Situational Awareness)", font=font_small, fill=(240, 196, 0))
save_both(crop_03, "evidence_gts03_pedestrian.png")

# 6. Slide 7: GTS07 Negative Sample (Empty Road - 0 Box)
img_gts07 = Image.open(os.path.join(gts_dir, "GTS07.png"))
crop_07 = img_gts07.resize((480, 260), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(crop_07)
draw.rounded_rectangle([130, 95, 350, 145], radius=6, fill=(43, 182, 115))
draw.text((145, 108), "0 ANNOTATION (NEGATIVE)", font=font_label, fill=(255, 255, 255))
draw.rectangle([0, crop_07.height - 24, crop_07.width, crop_07.height], fill=(16, 18, 16))
draw.text((10, crop_07.height - 20), "GTS07: Tuyệt đối không vẽ box khống vào bóng râm/khung cầu", font=font_small, fill=(240, 196, 0))
save_both(crop_07, "evidence_gts07_negative.png")

print("All visual assets finalized successfully!")
