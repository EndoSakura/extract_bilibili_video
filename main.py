import json
import os
import subprocess

def getTitle(partPath):
    if os.path.exists(partPath + "\\entry.json"):
        with open(partPath + "\\entry.json", 'r', encoding='utf-8') as file:
            ret_dic = json.load(file)
            title = ret_dic['title']
        return formatTitle(title)

def formatTitle(partTitle):
    partTitle = partTitle.replace(" ", "")
    partTitle = partTitle.replace("①", "1")
    partTitle = partTitle.replace("②", "2")
    partTitle = partTitle.replace("③", "3")
    partTitle = partTitle.replace("④", "4")
    partTitle = partTitle.replace("⑤", "5")
    partTitle = partTitle.replace("⑥", "6")
    partTitle = partTitle.replace("&", "-")
    partTitle = partTitle.replace(".", "_")
    return partTitle

def extracVideo(partPath, outputPath):
    if not os.path.exists(partPath + "\\entry.json"):
        return

    with open(partPath + "\\entry.json", 'r', encoding='utf-8') as file:
            ret_dic = json.load(file)
            page_data = ret_dic['page_data']
            type_tag =ret_dic['type_tag']
            videoTitle = ret_dic['title']
            partTitle = page_data['part']
            width = page_data['width']
            height = page_data['height']
            
    formatPartTitle = formatTitle(partTitle)
    outPutVideoName = formatPartTitle + ".mp4"
    outputVideoPath = outputPath + "\\" + outPutVideoName

    #提取弹幕文件
    if os.path.exists(partPath + "\\danmaku.xml"):
        outAssName = outputPath + "\\" + formatPartTitle + ".ass"
        print(outAssName)
        if os.path.exists(outAssName):
            print(outAssName + "已提取")
        else:
            import danmaku2ass #利用别人写好的danmaku2ass.py中的方法

            #高分辨率下，字体大一些
            fontSize = 23.0
            if width >= 1920:
                fontSize = 36.0

            danmaku2ass.Danmaku2ASS(partPath + "\\danmaku.xml","Bilibili" , outAssName, width, height,\
                reserve_blank=480,font_size=fontSize, text_opacity=1, duration_marquee=12.0, duration_still=6.0) #这些参数可调

    fileRealPath = partPath + "\\" + type_tag
    oldAudioPath = fileRealPath + "\\" + "audio.m4s"
    oldVideoPath = fileRealPath + "\\" + "video.m4s"
    newAudioPath = fileRealPath + "\\" + "audio.mp3"
    newVideoPath = fileRealPath + "\\" + "video.mp4"
    if os.path.exists(oldAudioPath):
        os.rename(oldAudioPath, newAudioPath)
    if os.path.exists(oldVideoPath):
        os.rename(oldVideoPath, newVideoPath)
    if os.path.exists(outputVideoPath):
        print(outputVideoPath + "已提取")
        return
    print(outputVideoPath)
    subprocess.call("ffmpeg " + "-i " + newVideoPath + " -i "+ newAudioPath + " -codec copy " + outputVideoPath, shell=True)


#begin
rootPath = os.getcwd() + "\\resource"
outputPath = os.getcwd() + "\\output"

for videoPath in os.listdir(rootPath):
    videoPath = rootPath + "\\" + videoPath
    if not os.path.isdir(videoPath) :
        continue
    parts = os.listdir(videoPath)
    if len(parts) < 1 :
        continue
    title = getTitle(videoPath + "\\" + parts[0])
    videoOutputPath = outputPath + "\\" + title;
    if not os.path.exists(videoOutputPath):
        os.makedirs(videoOutputPath)

    for partPath in parts:
        partPath = videoPath + "\\" + partPath;
        extracVideo(partPath, videoOutputPath)

