from catches.models import *
from catches.views import *
from PIL import Image, ImageOps, ExifTags
from PIL.ExifTags import TAGS

def reorient_img(pil_img):
    img_exif = pil_img.getexif()

    if len(img_exif):
        if img_exif[274] == 3:
            pil_img = pil_img.transpose(Image.ROTATE_180)
        elif img_exif[274] == 6:
            pil_img = pil_img.transpose(Image.ROTATE_270)
        elif img_exif[274] == 8:
            pil_img = pil_img.transpose(Image.ROTATE_90)

    return pil_img

def print_exif_data(exif_data):
    for tag_id in exif_data:
        tag = TAGS.get(tag_id, tag_id)
        content = exif_data.get(tag_id)
        print(f'{tag:25}: {content}')

def run():
    image = Image.open ("public/uploads/pictures/image_kNgIFO3.jpg")
    exif = image.getexif()
    
    print_exif_data(exif)
    print()
    print_exif_data(exif.get_ifd(0x8769))
    # image.show()
    # img_exif = image.getexif()
    # print (f'{img_exif = }')
    # # image_mod = reorient_img (image)
    # image_mod = image.transpose(Image.ROTATE_270)
    # image_mod.show()
    # image_mod.save ("public/uploads/pictures/mods/image_kNgIFO3.jpg")
    # image_mod.close()

