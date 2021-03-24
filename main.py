import json
import os
import subprocess
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
# https://docs.python.org/3/library/pathlib.html#concrete-paths
# use Path to make code universal between posix and Windows OS.
from pathlib import Path

def getTitle(partPath):
    partPath = Path(partPath)
    if os.path.exists(partPath / "entry.json"):
        with open(partPath / "entry.json", 'r', encoding='utf-8') as file:
            retDic = json.load(file)
            title = retDic['title']
        return formatTitle(title)

def formatTitle(partTitle):
    replaceDict = {" ": "", "①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6",
                   "&": "-", ".": "_", "（": "", "）": "", "(": "", ")": "", "-": "", "/": "_"}
    for key, value in replaceDict.items():
        partTitle = partTitle.replace(key, value)
    print("partTitle :" + str(partTitle))
    return partTitle

def extracVideo(partPath, outputPath):
    partPath = Path(partPath)
    outputPath = Path(outputPath)
    if not os.path.exists(partPath / "entry.json"):
        return

    with open(partPath / "entry.json", 'r', encoding='utf-8') as file:
            retDic = json.load(file)
            print("retDic:" + str(retDic))
            print("partPath:" + str(partPath))
            if ("page_data" not in retDic) or ("type_tag" not in retDic) or \
               ("title" not in retDic):
                return
            pageData = retDic['page_data']
            typeTag = retDic['type_tag']
            videoTitle = retDic['title']
            partTitle = pageData['part']
            width = pageData['width']
            height = pageData['height']

    formatPartTitle = formatTitle(partTitle)
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.with_suffix
    # PurePath.with_suffix(suffix)
    # Return a new path with the suffix changed. If the original path doesn’t have a suffix, the new suffix is appended instead. If the suffix is an empty string, the original suffix is removed:
    outPutVideoName = Path(formatPartTitle).with_suffix(".mp4")
    outputVideoPath = outputPath / outPutVideoName

    #extract danmu file
    if os.path.exists(partPath / "danmaku.xml"):
        outAssName = (outputPath / formatPartTitle).with_suffix(".ass")
        print(str(outAssName))
        if os.path.exists(outAssName):
            print(str(outAssName) + "extract down.")
        else:
            import danmaku2ass # reuse code in danmaku2ass.py

            # when high resolution, make font larger
            fontSize = 23.0
            if width >= 1920:
                fontSize = 36.0

            danmaku2ass.Danmaku2ASS(str(partPath / "danmaku.xml"), "Bilibili" , str(outAssName), width, height,\
                reserve_blank=480,font_size=fontSize, text_opacity=1, duration_marquee=12.0, duration_still=6.0) # to tune argus


    fileRealPath = partPath / typeTag
    oldAudioPath = fileRealPath / "audio.m4s"
    oldVideoPath = fileRealPath / "video.m4s"
    newAudioPath = fileRealPath / "audio.mp3"
    newVideoPath = fileRealPath / "video.mp4"

    if os.path.exists(oldAudioPath):
        os.rename(oldAudioPath, newAudioPath)
    if os.path.exists(oldVideoPath):
        os.rename(oldVideoPath, newVideoPath)
    if os.path.exists(outputVideoPath):
        print(str(outputVideoPath) + " extract done!")
        return
    print(outputVideoPath)
    # https://docs.python.org/3/library/subprocess.html
    # https://stackoverflow.com/questions/25655173/does-pythons-subprocess-popen-accept-spaces-in-paths
    # A string surrounded by double quotation marks is interpreted as a single argument, regardless of white space contained within. A quoted string can be embedded in an argument.
    subprocess.call('ffmpeg -i "%s" -i "%s" -codec copy "%s"' %(str(newVideoPath), str(newAudioPath), str(outputVideoPath)), shell=True)

if os.name == "nt":
    rootPath = Path(os.getcwd()) / "resource"
    outputPath = Path(os.getcwd()) / "output"
else: # "posix"
    rootPath = Path(os.getcwd()) / "resource_linux"
    outputPath = Path(os.getcwd()) / "output_linux"


for videoPath in os.listdir(rootPath):
    videoPath = rootPath / videoPath
    parts = os.listdir(videoPath)
    if len(parts) < 1 :
        continue
    title = getTitle(videoPath / parts[0])
    videoOutputPath = outputPath / str(title);
    if not os.path.exists(videoOutputPath):
        os.makedirs(videoOutputPath)

    for partPath in parts:
        partPath = videoPath / partPath;
        extracVideo(partPath, videoOutputPath)

