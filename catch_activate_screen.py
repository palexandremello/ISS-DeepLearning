import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import time
import win32con


def get_specific_window(name_of_app):
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    win32gui.EnumWindows(enum_cb, toplist)
    specific_app = [(hwnd, title) for hwnd, title in winlist if name_of_app in title.lower()]
    specific_app = specific_app[0]
    hwnd = specific_app[1]
    return hwnd

def grab_screen(name_of_app):
    app_name = get_specific_window('snes9x')
    hwnd_target = win32gui.FindWindow(None, app_name)
    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    w = right - left
    h = bot - top
    
    win32gui.SetForegroundWindow(hwnd_target)
    time.sleep(0.1)
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    if result == None:
        #PrintWindow Succeeded
        im.save("test.png")
