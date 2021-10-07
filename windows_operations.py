import os
from pathlib import Path
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image, ImageOps
import pyautogui

BASE_DIR = Path(__file__).resolve().parent

def take_screenshot(target_window):
    SOURCE_DIR = os.path.join(BASE_DIR, "static", "source.jpg")

    width = int(get_window_size(target_window)["width"])
    height = int(get_window_size(target_window)["height"])

    wDC = win32gui.GetWindowDC(target_window)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, SOURCE_DIR)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(target_window, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = Image.open(SOURCE_DIR)
    if width / height != 1920 / 1080:
        height_crop = height - 40
        width_crop = height_crop * 1920 / 1080

        screen_width, screen_height = pyautogui.size()
        if width == screen_width:
            side_border = (screen_width - 40) / 2 - width_crop / 2
            img_cropped = img.crop(
                (side_border, 40, side_border + width_crop, height_crop + 40)
            )
        else:
            img_cropped = img.crop((1, 40, width_crop, height_crop + 40 - 1))
        img_resize = img_cropped.resize((1920, 1080), Image.ANTIALIAS)
        img_resize.save(SOURCE_DIR)
    return


def get_window_size(target_window):
    rect = win32gui.GetWindowRect(target_window)
    x0, y0, x1, y1 = rect[0], rect[1], rect[2], rect[3]
    w, h = x1 - x0, y1-y0

    context = {
        "width": w,
        "height": h,
    }
    return context

def click(x, y, target_window):
    width = int(get_window_size(target_window)["width"])
    height = int(get_window_size(target_window)["height"])
    if width / height != 1920 / 1080:
        height = height - 40
        print(f"height: {height}")
        ratio = height / 1080
    else:
        ratio = 1
    print(f"x: {x}, y: {y}")
    x = x * ratio
    x = int(x)
    y = y * ratio
    y = int(y)
    print(f"x: {x}, y: {y}")
    lParam = win32api.MAKELONG(x, y)

    target_window1 = win32gui.FindWindowEx(target_window, None, None, None)
    win32gui.SendMessage(target_window1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(target_window1, win32con.WM_LBUTTONUP, None, lParam)
    return