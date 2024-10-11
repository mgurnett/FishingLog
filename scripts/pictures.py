from catches.models import *
from catches.views import *
from PIL import Image, ImageOps, ExifTags, ImageFilter
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

def print_exif_data(exifdata):
    for tag_id in exifdata:
        tag = TAGS.get(tag_id,tag_id)
        print(tag_id)
        data = exifdata.get(tag_id)
        # we decode bytes
        if isinstance(data,bytes):
            data = data.decode()
        print(f'{tag:25}: {data}')

def resize_picture (image, new_width):
    #Resize by maintaining aspect ratio (e.g., specify the width)
    aspect_ratio_preserved = image.resize((new_width, int(image.height * (new_width / image.width))))
    return aspect_ratio_preserved

def crop_pict (image, left, upper, right, lower ):
    #Define the coordinates for the region to be cropped (left, upper, right, lower)
 

    #Crop the image using the coordinates
    cropped_image = image.crop((left, upper, right, lower))
    return cropped_image

def run():
    images = [
        "blog_pict.png",
        "fly_rods.jpeg",
        "Mitchel.jpeg", #(image, 0, 44, 225, 212)
        "tiger-trout.jpeg",  #h_crop = 40 & 300
        "dragon_nymph.jpeg",
        "Parachute.png",
    ]
    # for im_name in images:
    #     image = Image.open ("public/assets/catches/site/back_up/" + im_name)
    #     image_mod = resize_picture (image)
    #     image_mod.save ("public/assets/catches/site/" + im_name)
    #     image_mod.close()

    im_name = "dragon_nymph.jpeg"
    image = Image.open ("public/assets/catches/site/back_up/" + im_name)
    image.save ("public/assets/catches/site/" + im_name)
    h_crop = 5
    image_mod = crop_pict (image, 0, h_crop, 252, h_crop+189)  #(left, upper, right, lower)
    image_mod.save ("public/assets/catches/site/crop_" + im_name)
    image_mod = image_mod.filter(ImageFilter.SHARPEN)
    image_mod.save ("public/assets/catches/site/sharpen_" + im_name)
    # image_mod = resize_picture (image_mod, 100)
    # image_mod.save ("public/assets/catches/site/resize_" + im_name)

    # image_mod.show()
    image_mod.close()
'''
    im_name = "Mitchel.jpeg"
    image = Image.open ("public/assets/catches/site/back_up/" + im_name)
    # image.save ("public/assets/catches/site/" + im_name)
    image_mod = crop_pict (image, 0, 44, 225, 212)  #(left, upper, right, lower)
    # image_mod.save ("public/assets/catches/site/crop_" + im_name)
    image_mod = image_mod.filter(ImageFilter.SHARPEN)
    # image_mod.save ("public/assets/catches/site/sharpen_" + im_name)
    image_mod = resize_picture (image_mod, 100)
    image_mod.save ("public/assets/catches/site/resize_" + im_name)

    # image_mod.show()
    image_mod.close()
'''




    # exif = image.getexif()
    
    # print_exif_data(exif)
    # print()
    # print_exif_data(exif.get_ifd(0x8769))
    # image.show()
    # img_exif = image.getexif()
    # print (f'{img_exif = }')
    # # image_mod = reorient_img (image)
    # image_mod = image.transpose(Image.ROTATE_270)
    # image_mod.show()
    # image_mod.save ("public/uploads/pictures/mods/image_kNgIFO3.jpg")
    # image_mod.close()



