from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
from schoology import *
import json

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.uploadButton = Button(self, text='Upload File to Schoology',
            command=self.upload)
        self.uploadButton.pack()

        self.downloadButton = Button(self, text='Download Attendance from Schoology',
        	command=self.download)
        self.downloadButton.pack()

        self.quitButton = Button(self, text='Quit',
            command=self.quit)
        self.quitButton.pack()

    def upload(self):
        filename = self.selectFile()
        if filename=="":
            return

    def download(self):
        data = fetchAllAttendance()
        with open('attendance_data.json', 'w') as f:
            f.write(json.dumps(data))

    def selectFile(self):
        filename = filedialog.askopenfilename()
        if filename != "": 
	        spot = filename.rfind("/")
	        os.chdir(filename[:spot])
	        filename = filename[spot+1:]
	        pprint(filename)
        return filename

app = Application()
app.master.title("JSerra Attendance Application")
app.master.minsize(400,400)
app.master.maxsize(400,400)