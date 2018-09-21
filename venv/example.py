#! /usr/bin/env python  
# -*- coding: utf-8 -*-  

#QQ send message auto

from pynput.mouse import Controller as Mouse
from pynput.mouse import Button as bt
from pynput.keyboard import Controller as Keyboard
from pynput.keyboard import Key 
import time


def TellHer(ms,kb):
    ms.position = (224,552)
    ms.press(bt.left)
    ms.release(bt.left)
    kb.type("diannaoyonghuzanshilikaile")
    kb.press(Key.space)
    kb.release(Key.space)
    kb.press(Key.enter)
    kb.release(Key.enter)
    time.sleep(0.3)
    kb.type("qingxianbuyaodongzhetaidiannaoo")
    kb.press(Key.space)
    kb.release(Key.space)
    kb.press(Key.enter)
    kb.release(Key.enter)
    time.sleep(0.3)
    kb.type("thanks!")
    kb.press(Key.space)
    kb.release(Key.space)
    kb.press(Key.enter)
    kb.release(Key.enter)

    kb.press(Key.ctrl)
    kb.type('v')
    kb.release(Key.ctrl)
    time.sleep(5)
    kb.press(Key.ctrl)
    kb.type('a')
    kb.release(Key.ctrl)
    time.sleep(3)
    kb.press(Key.backspace)
    kb.release(Key.backspace)


def main():
    ms=Mouse()
    kb=Keyboard()
    for i in range(2):
        TellHer(ms,kb);

if __name__ == '__main__':
    main()
