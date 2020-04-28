import webview
import signal
import time
import sys
import threading

"""
Adrian Rosoga, 6 Apr 2020

pip3 install pywebview --user

TODO - Error handling when page/web not available, add Refresh button, etc
TODO - Add the site that gave pynput idea
TODO - Remove the alerts "Memory pressure relief..."
TODO - Add requirements.txt, etc
TODO - Check why crash when sending signal
TODO - Use pyinstaller https://github.com/r0x0r/pyinstaller
TODO - See why high CPU with google.com
"""

from pynput import keyboard

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

def execute():
    print ("Reloading the page...")
    webview.windows[0].load_url("http://192.168.1.105:8007/tl")

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

default_handler = signal.getsignal(signal.SIGUSR1)

print(default_handler)

def handler(signum, frame):
    print(f'Received signal {signal}')
    #print(len(windows))
    #windows[0].load_url("http://google.com")


#signal.signal(signal.SIGUSR1, handler)

#time.sleep(10000)

#window = webview.create_window('Simple browser', 'http://google.com')
window = webview.create_window('Simple browser', 'http://192.168.1.105:8007/tl', x=0, y=0, min_size=(1840, 1240))
webview.start()
