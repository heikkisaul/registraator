import tkinter as tk
from tkinter import ttk

import random
from multiprocessing import Process, Value, Array
import os
import sys
import time

import rfid_data as rd
import esteid_data as ed

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

    sharedvar = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        startButton = ttk.Button(self, text="ALUSTA",command=self.start_cardlistener)
        startButton.grid(row=2, column=1,sticky = "nsew")


    def start_cardlistener(self):

        num0 = Value('i',0)
        num1 = Value('i', 0)

        self.p1 = Process(target=self.rfid_multiprocessing, args=(num0))
        self.p2 = Process(target=self.scard_multiprocessing, args=(num1))

        self.p1.start()
        self.p2.start()

        print(num0.value)
        print(num1.value)

    def rfid_multiprocessing(self, n):
        global sharedvar
        while True:
            result = rd.test_commit()
            n.value = 3
            print(result)

    def scard_multiprocessing(self, n):
        global sharedvar
        while True:
            result = ed.sc_test_commit()
            n.value = 2
            print(result)

app = Registrator()
app.mainloop()
