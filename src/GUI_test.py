import tkinter as tk
from tkinter import ttk

import random
from multiprocessing import Process
import os
import sys
import time

import rfid_data as rd

class Registrator(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.geometry(self,"320x480")

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LandingPage, AdminPage, NewLecturePage, CardRegPage, AddStudentPage, StudentPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(LandingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class LandingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        newLectButton = ttk.Button(self, text = "UUS LOENG", command = lambda : controller.show_frame(NewLecturePage))
        addCardButton = ttk.Button(self, text="REGISTREERI KAART", command = lambda : controller.show_frame(CardRegPage))
        closeButton = ttk.Button(self, text="SULGE")

        newLectButton.grid(row = 0, column = 1,sticky = "nsew")
        addCardButton.grid(row=1, column=1,sticky = "nsew")
        closeButton.grid(row=2, column=1,sticky = "nsew")

    #TODO make close button shut Raspi down

class NewLecturePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lectListBox = tk.Listbox(self)
        lectListScroll = ttk.Scrollbar(self)
        lectListBox.config(yscrollcommand=lectListScroll.set)
        lectListScroll.config(command=lectListBox.yview)
        lectListLabel = ttk.Label(self, text="Vali loeng")

        searchLectButton = ttk.Button(self, text="OTSI", command=lambda: controller.show_frame(AdminPage))
        selectLectButton = ttk.Button(self, text = "VALI LOENG", command = lambda : controller.show_frame(AdminPage))
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(LandingPage))

        lectListBox.grid(row=1, column=1,sticky = "nsew")
        lectListScroll.grid(row=1, column=2, sticky="nsew")
        lectListLabel.grid(row=0, column=1, sticky="nsew")
        selectLectButton.grid(row=2, column=1, sticky="nsew")
        selectLectButton.grid(row = 3, column = 1,sticky = "nsew")
        backButton.grid(row=4, column=1,sticky = "nsew")

    #TODO populate list on button press by searching from 'lectures' table in DB based on lecturer ID-code (lecturer must use ID-card)

class CardRegPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        nameEntry = ttk.Entry(self)
        codeEntry = ttk.Entry(self)


        selectButton = ttk.Button(self, text = "KINNITA", command = lambda : controller.show_frame(LandingPage))
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(LandingPage))

        nameEntry.grid(row=0, column=1, sticky="nsew")
        codeEntry.grid(row=1, column=1, sticky="nsew")
        selectButton.grid(row = 2, column = 1,sticky = "nsew")
        backButton.grid(row=3, column=1,sticky = "nsew")

class AdminPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        endLectButton = ttk.Button(self, text = "LÕPETA LOENG", command = lambda : controller.show_frame(LandingPage))
        addStudentButton = ttk.Button(self, text="LISA ÕPILANE", command = lambda : controller.show_frame(AddStudentPage))
        lockButton = ttk.Button(self, text="EKRAANILUKK", command = lambda : controller.show_frame(StudentPage))

        endLectButton.grid(row = 0, column = 1,sticky = "nsew")
        addStudentButton.grid(row=1, column=1,sticky = "nsew")
        lockButton.grid(row=2, column=1,sticky = "nsew")

class AddStudentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        selectButton = ttk.Button(self, text = "KINNITA", command = lambda : controller.show_frame(LandingPage))
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(AdminPage))

        nameEntry = ttk.Entry(self)
        codeEntry = ttk.Entry(self)

        nameEntry.grid(row=0, column=1, sticky="nsew")
        codeEntry.grid(row=1, column=1, sticky="nsew")

        selectButton.grid(row = 2, column = 1,sticky = "nsew")
        backButton.grid(row=3, column=1,sticky = "nsew")

class StudentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.p1 = Process(target=self.rfid_multiprocessing)
        self.p1.start()


    def multiprocessing_test(self):
        while True:
            time.sleep(3)
            print(random.randint(0, 999999999))

    def rfid_multiprocessing(self):
        result = rd.test_commit()
        print(result)


    #TODO add label to show ID-code or card code
    #TODO add mechanism to flash screen green on successful read

def multiprocessing_test():
    print(random.randint(0, 999999999))
    print()

if __name__ == "__main__":

    app = Registrator()
    app.mainloop()

    p2 = Process(target=multiprocessing_test)
    p3 = Process(target=multiprocessing_test)

    try:
        p2.start()
        p3.start()
        #os.execv(sys.executable,['python3'] + sys.argv)

    except:
        #os.execv(sys.executable, ['python3'] + sys.argv)
        print("exception")

    #app = Registrator()
    #app.mainloop()
