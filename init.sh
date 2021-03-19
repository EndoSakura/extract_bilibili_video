#!/bin/bash

adb pull /sdcard/Android/data/com.bilibili.app.in ~/Downloads/Android/data/

ln -sf ~/Downloads/Android/data/com.bilibili.app.in/download resource_linux
ln -sf ~/Videos/ output_linux 

python ./main_linux.py
