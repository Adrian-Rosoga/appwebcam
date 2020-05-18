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
TODO - High CPU with google.com
"""

WEBSITE = "http://192.168.1.105:8007/tl"
# WEBSITE = 'http://google.com'
SIGNAL = signal.SIGILL
REFRESH_INTERVAL_SECS = 15


# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='a')},
    {keyboard.Key.ctrl, keyboard.KeyCode(char='A')}
]

COMBINATIONS = [
    {keyboard.Key.f5}
]


# The currently active modifiers
current = set()


def reload_page():
    print("Reloading the page...")
    webview.windows[0].load_url(WEBSITE)


def refresh():
    while True:
        time.sleep(REFRESH_INTERVAL_SECS)
        reload_page()


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            reload_page()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


def key_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


listener_thread = threading.Thread(target=key_listener, daemon=True)
listener_thread.start()

sys.stderr = sys.stdout

#
# On Windows, signal() can only be called with SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, or SIGTERM. A ValueError will be raised in any other case.
#
default_handler = signal.getsignal(SIGNAL)
print(default_handler)


def handler(signum, frame):
    print(f'Received signal {signal}')
    reload_page()


signal.signal(SIGNAL, handler)

# For Acer Swift
# window = webview.create_window('AppWebCam ({SEBSITE})', WEBSITE, x=0, y=0, min_size=(1840, 1240))

refresh_thread = threading.Thread(target=refresh, daemon=True)
refresh_thread.start()

# For Windows
window = webview.create_window(f'AppWebCam ({WEBSITE})', WEBSITE, x=110, y=10, min_size=(1840, 1100))

webview.start()
