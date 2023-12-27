import torch
import json
import os
import re
import platform
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import safetensors.torch


def get_img_path(template_name, template_type):
    p = os.path.dirname(os.path.realpath(__file__))
    # 根据操作系统选择合适的分隔符
    if os.name == 'posix':  # Unix/Linux/macOS
        separator = '/'
    elif os.name == 'nt':  # Windows
        separator = '\\'
    else:
        separator = '/'  # 默认使用斜杠作为分隔符

    image_path = os.path.join(p, 'img_lists', template_type)  # 使用适当的分隔符构建路径
    image_filename = f"{template_name}.jpg"

    full_image_path = image_path + separator + image_filename

    return full_image_path


class ArtistsImage_Zho:
    @classmethod
    def INPUT_TYPES(s):
        p = os.path.dirname(os.path.realpath(__file__))
        atsimg_dir = os.path.join(p, 'img_lists/artists/')
        files = [f for f in os.listdir(atsimg_dir) if os.path.isfile(os.path.join(atsimg_dir, f))]

        max_float_value = 1.75

        return {
            "required": {
                "image": (sorted(files), {"image_upload_artist": True}),
                "weight": ("FLOAT", {
                    "default": 1.2,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
               }),
            }
        }


    CATEGORY = "Zho模块组/🎨 ArtGallery 艺术画廊"

    RETURN_TYPES = ("STRING", "IMAGE",)
    RETURN_NAMES = ("name", "image",)
    FUNCTION = "artists_image"

    def artists_image(self, image, weight=1):
        image_full_name = image
        image_name = image_full_name.rsplit('.', 1)[0]

        image_path =  get_img_path(image_name, "artists")
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        prompt = []

        if weight > 0:
            P_artist = f"({image_name}:{round(weight, 2)})"
            prompt.append(P_artist)

        return (P_artist, output_image,)


    @classmethod
    def IS_CHANGED(s, image):
        image_path = get_img_path(image_name, "artists")
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()


class CamerasImage_Zho:
    @classmethod
    def INPUT_TYPES(s):
        p = os.path.dirname(os.path.realpath(__file__))
        camerasimg_dir = os.path.join(p, 'img_lists/cameras/')
        files = [f for f in os.listdir(camerasimg_dir) if os.path.isfile(os.path.join(camerasimg_dir, f))]

        max_float_value = 1.75

        return {
            "required": {
                "image": (sorted(files), {"image_upload_camera": True}),
                "weight": ("FLOAT", {
                    "default": 1.2,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
               }),
            }
        }


    CATEGORY = "Zho模块组/🎨 ArtGallery 艺术画廊"

    RETURN_TYPES = ("STRING", "IMAGE",)
    RETURN_NAMES = ("name", "image",)
    FUNCTION = "cameras_image"

    def cameras_image(self, image, weight=1):
        image_full_name = image
        image_name = image_full_name.rsplit('.', 1)[0]

        image_path =  get_img_path(image_name, "cameras")
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        prompt = []

        if weight > 0:
            P_camera = f"({image_name}:{round(weight, 2)})"
            prompt.append(P_camera)

        return (P_camera, output_image,)


    @classmethod
    def IS_CHANGED(s, image):
        image_path = get_img_path(image_name, "cameras")
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()


class FilmsImage_Zho:
    @classmethod
    def INPUT_TYPES(s):
        p = os.path.dirname(os.path.realpath(__file__))
        filmsimg_dir = os.path.join(p, 'img_lists/films/')
        files = [f for f in os.listdir(filmsimg_dir) if os.path.isfile(os.path.join(filmsimg_dir, f))]

        max_float_value = 1.75

        return {
            "required": {
                "image": (sorted(files), {"image_upload_film": True}),
                "weight": ("FLOAT", {
                    "default": 1.2,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
               }),
            }
        }


    CATEGORY = "Zho模块组/🎨 ArtGallery 艺术画廊"

    RETURN_TYPES = ("STRING", "IMAGE",)
    RETURN_NAMES = ("name", "image",)
    FUNCTION = "films_image"

    def films_image(self, image, weight=1):
        image_full_name = image
        image_name = image_full_name.rsplit('.', 1)[0]

        image_path =  get_img_path(image_name, "films")
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        prompt = []

        if weight > 0:
            P_film = f"({image_name}:{round(weight, 2)})"
            prompt.append(P_film)

        return (P_film, output_image,)


    @classmethod
    def IS_CHANGED(s, image):
        image_path = get_img_path(image_name, "films")
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

class MovementsImage_Zho:
    @classmethod
    def INPUT_TYPES(s):
        p = os.path.dirname(os.path.realpath(__file__))
        movementsimg_dir = os.path.join(p, 'img_lists/movements/')
        files = [f for f in os.listdir(movementsimg_dir) if os.path.isfile(os.path.join(movementsimg_dir, f))]

        max_float_value = 1.75

        return {
            "required": {
                "image": (sorted(files), {"image_upload_movement": True}),
                "weight": ("FLOAT", {
                    "default": 1.2,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
               }),
            }
        }


    CATEGORY = "Zho模块组/🎨 ArtGallery 艺术画廊"

    RETURN_TYPES = ("STRING", "IMAGE",)
    RETURN_NAMES = ("name", "image",)
    FUNCTION = "movements_image"

    def movements_image(self, image, weight=1):
        image_full_name = image
        image_name = image_full_name.rsplit('.', 1)[0]

        image_path =  get_img_path(image_name, "movements")
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        prompt = []

        if weight > 0:
            P_movement = f"({image_name}:{round(weight, 2)})"
            prompt.append(P_movement)

        return (P_movement, output_image,)


    @classmethod
    def IS_CHANGED(s, image):
        image_path = get_img_path(image_name, "movements")
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()


class StylesImage_Zho:
    @classmethod
    def INPUT_TYPES(s):
        p = os.path.dirname(os.path.realpath(__file__))
        stylesimg_dir = os.path.join(p, 'img_lists/styles/')
        files = [f for f in os.listdir(stylesimg_dir) if os.path.isfile(os.path.join(stylesimg_dir, f))]

        max_float_value = 1.75

        return {
            "required": {
                "image": (sorted(files), {"image_upload_style": True}),
                "weight": ("FLOAT", {
                    "default": 1.2,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
               }),
            }
        }


    CATEGORY = "Zho模块组/🎨 ArtGallery 艺术画廊"

    RETURN_TYPES = ("STRING", "IMAGE",)
    RETURN_NAMES = ("name", "image",)
    FUNCTION = "styles_image"

    def styles_image(self, image, weight=1):
        image_full_name = image
        image_name = image_full_name.rsplit('.', 1)[0]

        image_path =  get_img_path(image_name, "styles")
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        prompt = []

        if weight > 0:
            P_style = f"({image_name}:{round(weight, 2)})"
            prompt.append(P_style)

        return (P_style, output_image,)


    @classmethod
    def IS_CHANGED(s, image):
        image_path = get_img_path(image_name, "styles")
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()


NODE_CLASS_MAPPINGS = {
    "ArtistsImage_Zho": ArtistsImage_Zho,
    "CamerasImage_Zho": CamerasImage_Zho,
    "FilmsImage_Zho": FilmsImage_Zho,
    "MovementsImage_Zho": MovementsImage_Zho,
    "StylesImage_Zho": StylesImage_Zho,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ArtistsImage_Zho": "🎨 ArtistsGallery_Zho",
    "CamerasImage_Zho": "🎨 CamerasGallery_Zho",
    "FilmsImage_Zho": "🎨 FilmsGallery_Zho",
    "MovementsImage_Zho": "🎨 MovementsGallery_Zho",
    "StylesImage_Zho": "🎨 StylesGallery_Zho",

}



