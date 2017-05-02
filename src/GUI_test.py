import tkinter as tk
from tkinter import ttk

import random
from multiprocessing import Process, Queue
import queue
import os
import sys
import time

import rfid_data as rd
import esteid_data as ed
from vars import *

class Registrator(tk.Tk):

    def __init__(self,*args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.geometry(self,"320x480")
        tk.Tk.resizable(self, False, False)
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
        newLectButton = ttk.Button(self, text = "UUS LOENG", command = lambda : controller.show_frame(NewLecturePage),width=51)
        addCardButton = ttk.Button(self, text="REGISTREERI KAART", command = lambda : controller.show_frame(CardRegPage),width=51)
        closeButton = ttk.Button(self, text="SULGE",width=51)

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

        searchLectButton = ttk.Button(self, text="OTSI", command=lambda: controller.show_frame(AdminPage),width=51)
        selectLectButton = ttk.Button(self, text = "VALI LOENG", command = lambda : controller.show_frame(AdminPage),width=51)
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(LandingPage),width=51)

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

        fnameEntry = ttk.Entry(self)
        mnameEntry = ttk.Entry(self)
        lnameEntry = ttk.Entry(self)
        codeEntry = ttk.Entry(self)

        fnameLabel = ttk.Label(self, text="Eesnimi")
        mnameLabel = ttk.Label(self, text="Keskmine nimi")
        lnameLabel = ttk.Label(self, text="Perekonnanimi")
        codeLabel = ttk.Label(self, text="Isikukood")

        selectButton = ttk.Button(self, text = "KINNITA", command = lambda : controller.show_frame(LandingPage),width=51)
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(LandingPage),width=51)

        fnameEntry.grid(row=1, column=1, sticky="nsew")
        mnameEntry.grid(row=3, column=1, sticky="nsew")
        lnameEntry.grid(row=5, column=1, sticky="nsew")

        fnameLabel.grid(row=0, column=1, sticky="nsew")
        mnameLabel.grid(row=2, column=1, sticky="nsew")
        lnameLabel.grid(row=4, column=1, sticky="nsew")
        codeLabel.grid(row=6, column=1, sticky="nsew")

        codeEntry.grid(row=7, column=1, sticky="nsew")
        selectButton.grid(row = 8, column = 1,sticky = "nsew")
        backButton.grid(row=9, column=1,sticky = "nsew")

class AdminPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        endLectButton = ttk.Button(self, text = "LÕPETA LOENG", command = lambda : controller.show_frame(LandingPage),width=51)
        addStudentButton = ttk.Button(self, text="LISA ÕPILANE", command = lambda : controller.show_frame(AddStudentPage),width=51)
        lockButton = ttk.Button(self, text="EKRAANILUKK", command = lambda : controller.show_frame(StudentPage),width=51)

        endLectButton.grid(row = 0, column = 1,sticky = "nsew")
        addStudentButton.grid(row=1, column=1,sticky = "nsew")
        lockButton.grid(row=2, column=1,sticky = "nsew")

class AddStudentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        fnameEntry = ttk.Entry(self)
        mnameEntry = ttk.Entry(self)
        lnameEntry = ttk.Entry(self)
        codeEntry = ttk.Entry(self)

        fnameLabel = ttk.Label(self, text="Eesnimi")
        mnameLabel = ttk.Label(self, text="Keskmine nimi")
        lnameLabel = ttk.Label(self, text="Perekonnanimi")
        codeLabel = ttk.Label(self, text="Isikukood")

        selectButton = ttk.Button(self, text = "KINNITA", command = lambda : controller.show_frame(AdminPage),width=51)
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(AdminPage),width=51)

        fnameEntry.grid(row=1, column=1, sticky="nsew")
        mnameEntry.grid(row=3, column=1, sticky="nsew")
        lnameEntry.grid(row=5, column=1, sticky="nsew")

        fnameLabel.grid(row=0, column=1, sticky="nsew")
        mnameLabel.grid(row=2, column=1, sticky="nsew")
        lnameLabel.grid(row=4, column=1, sticky="nsew")
        codeLabel.grid(row=6, column=1, sticky="nsew")

        codeEntry.grid(row=7, column=1, sticky="nsew")
        selectButton.grid(row = 8, column = 1,sticky = "nsew")
        backButton.grid(row=9, column=1,sticky = "nsew")

class StudentPage(tk.Frame):

    sharedvar = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.queue = q

        infoLabel = tk.Label(self, width=51, height=5)
        infoLabel.grid(row=1, column=0,sticky = "nsew")

        startButton = ttk.Button(self, text="ALUSTA",width=51,command=self.start_cardlistener)
        startButton.grid(row=2, column=0,sticky = "nsew")

        self.infoLabel = infoLabel

    def show_confirmation(self):
        self.infoLabel.config(background='lightgreen')
        self.after(500, self.restore_default)

    def restore_default(self):
        self.infoLabel.config(background='SystemMenu')


    def start_cardlistener(self):
        q = Queue()

        self.p1 = Process(target=self.rfid_multiprocessing, args=(self.queue,))

        self.p2 = Process(target=self.scard_multiprocessing, args=(self.queue,))

        self.p1.start()
        self.p2.start()

        self.after(100, func=self.show_info)

        #self.after(100, self.show_info)

    def show_info(self):

        if self.p2.is_alive() and self.p1.is_alive():
            try:
                #print(val)
                self.infoLabel.config(text=self.queue.get(0))
            except:
                print("error")
            self.after(100, func=self.show_info)
            return
        else:
            return

    def rfid_multiprocessing(self, queue):

        while True:
            result = rd.test_commit()
            try:
                pass
                queue.put(result[RFID_SERIALNO])

            except:
                pass

    def scard_multiprocessing(self, queue):

        while True:
            result = ed.sc_test_commit()

            try:
                pass
                queue.put(result[EID_IDCODE])

            except:
                pass

q = Queue()

app = Registrator()
app.mainloop()
