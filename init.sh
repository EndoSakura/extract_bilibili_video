#!/bin/bash

adb pull /sdcard/Android/data/com.bilibili.app.in ~/Downloads/Android/data/

ln -sf ~/Downloads/Android/data/com.bilibili.app.in/download resource
ln -sf ~/Videos/ output 

python ./main_linux.py
