import os

AD_TEXT_PATH = f"{os.getcwd()}/tg_bot/advertising_files/advertising_text.txt"
PICTURE_PATH = f"{os.getcwd()}/tg_bot/advertising_files/advertising_picture.jpg"


def create_files_for_advertising():
    with open(AD_TEXT_PATH, "r") as file:
        advertising_text = file.read()
    return advertising_text, PICTURE_PATH
