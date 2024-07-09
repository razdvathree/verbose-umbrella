import textwrap

from PIL import Image, ImageFont, ImageDraw
import numpy as np


def determine_image_brightness(image_path: str) -> float:
    """
    Determine the brightness of the image
    :param image_path: path to the image
    :return: brightness
    """
    img = Image.open(image_path)
    # Преобразуем изображение в оттенки серого
    gray = img.convert('L')
    mean = np.mean(np.array(gray))
    # Получаем либо 1 либо 0 в зависимости от яркости изображения
    return 1 - mean / 255


def wrap_text(text, width) -> list:
    """
    Wrap text to fit into image

    :param text:
    :param width:
    :return: lines, font
    """
    lines = textwrap.wrap(text, width)
    return lines


def add_text_to_image(image_path: str, text: str, save_path: str, color: tuple) -> None:
    """
    Add text to image

    :param color: rgb code of color to add
    :param image_path: path to the image
    :param text: text to add
    :param save_path: path to save image
    :return: None
    """
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    lines = wrap_text(text, 100)
    if img.width > 1000:
        size = 50
    else:
        size = 20
    x = 10
    y = 10
    font = ImageFont.truetype("arial.ttf", size=size)
    for line in lines:
        draw.text((x, y), line, color, font=font)
        y += font.getbbox(line)[3]
    img.save(save_path)
    return None


def add_text_to_image_with_brightness(image_path: str, text: str, save_path: str) -> None:
    """
    Add text to image with brightness

    :param image_path: path to the image
    :param text: text to add
    :param save_path: path to save image
    :return: None
    """
    brightness = determine_image_brightness(image_path)
    if brightness < 0.5:
        add_text_to_image(image_path, text, save_path, (255, 255, 255))
    else:
        add_text_to_image(image_path, text, save_path, (0, 0, 0))
