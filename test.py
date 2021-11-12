from PIL import Image as IImage
import pytesseract
import os, json
from datetime import datetime
from PIL import ImageTk
from tkinter import *
import tkinter
import time
import pyttsx3
import threading
from tkinter import ttk
import asyncio
from tkinter import filedialog
def ocr_core(filename):
    text = pytesseract.image_to_string(IImage.open(filename), lang='tur')
    return text

def format():
    listOfFiles = os.listdir(path='pagess')
    x = 0
    for file in sorted(listOfFiles):
        img = IImage.open("pagess/" + file)
        width, height = img.size
        img_left_area = (0, 0, (width/2), height)
        img_right_area = ((width/2), 0, width, height)
        img_left = img.crop(img_left_area)
        img_right = img.crop(img_right_area)
        img_left.save("pagess/" + str(x) + ".jpg")
        x+=1
        img_right.save("pagess/" + str(x) + ".jpg")
        x+=1
        os.unlink("pagess/" + file)
    return True

pages = list()
start = round(datetime.now().timestamp())
listOfFiles = os.listdir(path='pagess')
listOfFiles = str(json.dumps(listOfFiles)).replace(".jpg", "")
listOfFiles = json.loads(listOfFiles)
listOfFiles = [int(i) for i in listOfFiles]

#for page in sorted(listOfFiles):
    #page_text = ocr_core("pages/" + str(page) + ".jpg")
    #open("texts/"+str(page)+".txt", "a").write(page_text)
    #pages.append(page_text)

pages = sorted(listOfFiles)

for x in pages:
    pages[x] = ("pagess/" + str(x) + ".jpg")

window = Tk()
window.title("BookReader v1.0")
window.geometry("1400x800")

nowPage1 = 0
nowPage2 = 1

bookPagesFrame = ttk.LabelFrame(window, text="")
bookPagesFrame.pack(side = "right", fill = "both", expand = "yes")
pageSide1 = ttk.Label(bookPagesFrame)
pageSide2 = ttk.Label(bookPagesFrame)

def addPages(pageNum, side):
    pageImg1 = IImage.open(str(pages[int(pageNum)]))
    pageImg1 = pageImg1.resize((500, 700), IImage.ANTIALIAS)
    page1 = ImageTk.PhotoImage(pageImg1)
    if side == "left":
        pageSide1.configure(image=page1)
        pageSide1.image=page1
    else:
        pageSide2.configure(image=page1)
        pageSide2.image=page1

def setPages():
    global nowPage1, nowPage2
    addPages(nowPage1, "left")
    addPages(nowPage2, "right")

def previousPage():
    global nowPage1, nowPage2
    nowPage1 = nowPage1 - 2
    nowPage2 = nowPage2 - 2
    setPages()

def nextPage():
    global nowPage1, nowPage2
    nowPage1 = nowPage1 + 2
    nowPage2 = nowPage2 + 2
    setPages()

def start():
    global nowPage1, nowPage2
    nowPage1 = 0
    nowPage2 = 1
    addPages(nowPage1, "left")
    addPages(nowPage2, "right")
    buttonStart.configure(text="Reset")

manageFrame = ttk.LabelFrame(window, text="")
manageFrame.pack(side = "left", fill = "both", expand = "yes")

buttonStart = ttk.Button(manageFrame, text ="Start", command=lambda:start())
buttonStart.grid(column=1, row=0)

buttonNext = ttk.Button(manageFrame, text ="→", command=lambda:nextPage())
buttonNext.grid(column=1, row=1)

buttonPrevious = ttk.Button(manageFrame, text ="←", command=lambda:previousPage())
buttonPrevious.grid(column=1, row=2)

pageSide1.pack(side="left", fill="both", expand="yes")
pageSide2.pack(side="right", fill="both", expand="yes")

def startReading():
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.yelda.premium')
    engine.setProperty('rate', 185)
    engine.startLoop()
    turn = 0
    while True:
        global nowPage1
        if nowPage2 == len(pages):
            break
        if engine.isBusy()==False:
            if turn ==1:
                nowPage1 = nowPage1 -2
                nextPage()
                turn = 0
            print(nowPage1)
            page_text = ocr_core(pages[nowPage1])
            engine.say(page_text)
            booli = nowPage1%2==0
            if booli == False:
                turn = 1
            nowPage1 = nowPage1 +1
        time.sleep(1)

threads = list()

def readingThread():
    threading.Thread(target=startReading, daemon=True, args = ()).start()

buttonStartReading = ttk.Button(manageFrame, text ="Start Reading", command=lambda:readingThread())
buttonStartReading.grid(column=1, row=3)

buttonStopReading = ttk.Button(manageFrame, text ="Stop Reading", command=lambda:print(threads))
buttonStopReading.grid(column=1, row=4)

window.mainloop()