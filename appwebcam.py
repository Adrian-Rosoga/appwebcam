import webview
import signal
import time
import sys
import threading
from pynput import keyboard

"""
Adrian Rosoga, 6 Apr 2020

TODO - Error handling when page/web not available, add Refresh button, etc
TODO - Add the site that gave pynput idea
TODO - Remove the alerts "Memory pressure relief..."
TODO - Check why crash when sending signal
TODO - Use pyinstaller https://github.com/r0x0r/pyinstaller
TODO - See why high CPU with google.com
"""

WEBSITE = "http://192.168.1.105:8007/tl"
# WEBSITE = 'http://google.com'

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='a')},
    {keyboard.Key.ctrl, keyboard.KeyCode(char='A')}
]

COMBINATIONS = [
    {keyboard.Key.f5}
]


SIGNAL = signal.SIGILL


# The currently active modifiers
current = set()


def execute():
    print("Reloading the page...")
    webview.windows[0].load_url(WEBSITE)


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


def key_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


thr = threading.Thread(target=key_listener, daemon=True)
thr.start()

sys.stderr = sys.stdout

#
# On Windows, signal() can only be called with SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, or SIGTERM. A ValueError will be raised in any other case.
#
default_handler = signal.getsignal(SIGNAL)
print(default_handler)


def handler(signum, frame):
    print(f'Received signal {signal}')
    print(len(windows))
    windows[0].load_url(WEBSITE)


signal.signal(SIGNAL, handler)

# For Acer Swift
# window = webview.create_window('AppWebCam', WEBSITE, x=0, y=0, min_size=(1840, 1240))

# For Windows
window = webview.create_window('AppWebCam', WEBSITE, x=110, y=10, min_size=(1840, 1100))

webview.start()
