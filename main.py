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

    outPutVideoName = formatTitle(partTitle) + ".mp4"
    outputVideoPath = outputPath + "\\" + outPutVideoName

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