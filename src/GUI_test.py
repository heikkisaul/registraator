import tkinter as tk
from tkinter import ttk

import random
from multiprocessing import Process, Queue
import queue
import os
import sys
import time
import datetime
import pymysql

import rfid_data as rd
import esteid_data as ed
from vars import *

lecturer_id = 0
lecture_id = 0
lecture_data = ""

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
        newLectButton = ttk.Button(self, text = "UUS LOENG", command = lambda : controller.show_frame(NewLecturePage),width=40)
        addCardButton = ttk.Button(self, text="REGISTREERI KAART", command = lambda : controller.show_frame(CardRegPage),width=40)
        closeButton = ttk.Button(self, text="SULGE",width=40)

        newLectButton.grid(row = 0, column = 1,sticky = "nsew")
        addCardButton.grid(row=1, column=1,sticky = "nsew")
        closeButton.grid(row=2, column=1,sticky = "nsew")

    #TODO make close button shut Raspi down

class NewLecturePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lectListBox = tk.Listbox(self, selectmode='single')
        lectListScroll = ttk.Scrollbar(self)
        lectListBox.config(yscrollcommand=lectListScroll.set)
        lectListScroll.config(command=lectListBox.yview)
        lectListLabel = ttk.Label(self, text="Vali loeng")

        searchLectButton = ttk.Button(self, text="OTSI", command=self.get_lecture_list,width=37)
        selectLectButton = ttk.Button(self, text = "VALI LOENG", command = self.get_selected_lecture,width=37)
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(LandingPage),width=37)

        lectListBox.grid(row=1, column=1,sticky = "nsew")
        lectListScroll.grid(row=1, column=2, sticky="nsew")
        lectListLabel.grid(row=0, column=1, sticky="nsew")
        searchLectButton.grid(row=2, column=1, sticky="nsew")
        selectLectButton.grid(row=3, column=1, sticky="nsew")
        selectLectButton.grid(row = 4, column = 1,sticky = "nsew")
        backButton.grid(row=5, column=1,sticky = "nsew")

        self.lectListBox = lectListBox
        self.controller = controller

    def get_lecturer_id(self):
        lecturer_id = ed.sc_parse(ed.get_data())[0][3]
        return lecturer_id

    def get_lecture_list(self):
        global lecturer_id
        lect_list=[]
        lecturer_id = self.get_lecturer_id()
        conn = pymysql.connect(host='127.0.0.1', port=9990, user=DB_USR, passwd=DB_PWD,
                               db=DB_NAME)
        cur = conn.cursor()
        cur.execute("CALL `lect_reg_base`.`GET_TEACHER_LECTURES`({});".format(lecturer_id))
        print(cur.description)

        ctr=0

        for row in cur:
            lect_list.append(row)


        for row in lect_list:
            p_row = (row[0], row[1], row[3])

            self.lectListBox.insert(ctr, p_row)
            ctr+=1

        cur.close()
        conn.close()

        self.lect_list = lect_list


    def get_selected_lecture(self):
        global lecture_data
        global lecture_id
        selected = self.lectListBox.curselection()
        selection_id = selected[0]
        lecture_raw = self.lect_list[selection_id]
        lecture_id = lecture_raw[1]
        lecture_data="{}\n{}\n{}".format(lecture_raw[0],lecture_raw[3], lecture_raw[2])

        self.controller.show_frame(AdminPage)
        self.lectListBox.delete(0, tk.END)

class CardRegPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        codeEntry = ttk.Entry(self)
        rfidEntry = ttk.Entry(self)

        codeLabel = ttk.Label(self, text="Isikukood")
        rfidLabel = ttk.Label(self, text="Kaardikood")

        selectButton = ttk.Button(self, text = "KINNITA", command = self.reg_card,width=40)
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(LandingPage),width=40)

        codeEntry.grid(row=2, column=1, sticky="nsew")
        rfidEntry.grid(row=4, column=1, sticky="nsew")

        codeLabel.grid(row=1,column=1, sticky="nsew")
        rfidLabel.grid(row=3, column=1, sticky="nsew")

        selectButton.grid(row = 5, column = 1,sticky = "nsew")
        backButton.grid(row=6, column=1,sticky = "nsew")

        self.codeEntry = codeEntry
        self.rfidEntry = rfidEntry
        self.controller = controller

    def reg_card(self):
        code = self.codeEntry.get()
        rfid = self.rfidEntry.get()

        conn = pymysql.connect(host='127.0.0.1', port=9990, user=DB_USR, passwd=DB_PWD,
                               db=DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO CARD_DATA (CARD_CODE, ID_CODE) VALUES ({}, {});".format(rfid, code))
        conn.commit()
        print(cur.description)

        cur.close()
        conn.close()

        self.controller.show_frame(LandingPage)

class AdminPage(tk.Frame):

    def __init__(self, parent, controller):

        global lecture_data

        tk.Frame.__init__(self, parent)
        lectDataLabel = tk.Label(self, text = lecture_data)
        endLectButton = ttk.Button(self, text = "LÕPETA LOENG", command = lambda : controller.show_frame(LandingPage),width=40)
        addStudentButton = ttk.Button(self, text="LISA ÕPILANE", command = lambda : controller.show_frame(AddStudentPage),width=40)
        lockButton = ttk.Button(self, text="EKRAANILUKK", command = lambda : controller.show_frame(StudentPage),width=40)

        lectDataLabel.grid(row = 0, column = 1, sticky = "nsew")
        endLectButton.grid(row = 1, column = 1,sticky = "nsew")
        addStudentButton.grid(row=2, column=1,sticky = "nsew")
        lockButton.grid(row=3, column=1,sticky = "nsew")

        self.lectDataLabel = lectDataLabel
        self.refresh_lect_data()

    def refresh_lect_data(self):

        global lecture_data

        self.lectDataLabel.config(text= lecture_data)
        self.after(250,self.refresh_lect_data)

class AddStudentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        fnameEntry = ttk.Entry(self)
        lnameEntry = ttk.Entry(self)
        codeEntry = ttk.Entry(self)

        fnameLabel = ttk.Label(self, text="Eesnimi")
        lnameLabel = ttk.Label(self, text="Perekonnanimi")
        codeLabel = ttk.Label(self, text="Isikukood")

        selectButton = ttk.Button(self, text = "KINNITA", command = self.reg_student,width=40)
        backButton = ttk.Button(self, text="TAGASI", command = lambda : controller.show_frame(AdminPage),width=40)

        fnameEntry.grid(row=1, column=1, sticky="nsew")
        lnameEntry.grid(row=3, column=1, sticky="nsew")

        fnameLabel.grid(row=0, column=1, sticky="nsew")
        lnameLabel.grid(row=2, column=1, sticky="nsew")
        codeLabel.grid(row=4, column=1, sticky="nsew")

        codeEntry.grid(row=5, column=1, sticky="nsew")
        selectButton.grid(row = 6, column = 1,sticky = "nsew")
        backButton.grid(row=7, column=1,sticky = "nsew")

        self.fnameEntry = fnameEntry
        self.lnameEntry = lnameEntry
        self.codeEntry = codeEntry

    def reg_student(self):
        global lecture_id

        fname = self.fnameEntry.get()
        lname = self.lnameEntry.get()
        id_code = self.codeEntry.get()
        timestamp = datetime.datetime.now()
        str_timestamp = '%Y-%m-%d %H:%M:%S'.format(timestamp)

        f = open('data.log', 'a+')
        f.write("%s; %s; %s; %s; %s\n" % (str_timestamp, MANUAL_REG, id_code, fname.upper(),lname.upper()))
        f.close()

        conn = pymysql.connect(host='127.0.0.1', port=9990, user=DB_USR, passwd=DB_PWD,
                               db=DB_NAME)
        cur = conn.cursor()

        cur.execute("INSERT INTO LECTURE_VISIT (ID_CODE, LECTURE_ID, REG_TIMESTAMP) VALUES ({}, {}, {});".format(id_code, lecture_id, timestamp.strftime('\'%Y-%m-%d %H:%M:%S\'')))
        conn.commit()
        print(cur.description)

        cur.close()
        conn.close()

class StudentPage(tk.Frame):

    sharedvar = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.queue = q

        infoLabel = tk.Label(self, width=40, height=5)
        infoLabel.grid(row=1, column=0,sticky = "nsew")

        startButton = ttk.Button(self, text="ALUSTA",width=40,command=self.start_cardlistener)
        startButton.grid(row=2, column=0,sticky = "nsew")

        self.infoLabel = infoLabel
        self.controller = controller
        self.startButton = startButton

    def show_confirmation(self):
        self.infoLabel.config(background='lightgreen')
        self.after(500, self.restore_default)

    def restore_default(self):
        self.infoLabel.config(background=BGCOLOR)
        self.infoLabel.config(text="")


    def start_cardlistener(self):

        self.startButton.config(state='disabled')

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
                queue_val = self.queue.get(0)
                self.queue_val = queue_val
                self.infoLabel.config(text=self.queue_val)
                self.show_confirmation()
                self.stop_register()

            except:
                pass
                #print("error")
            self.after(100, func=self.show_info)
            return
        else:
            return

    def stop_register(self):
        global lecturer_id

        if self.queue_val == lecturer_id:
            self.p1.terminate()
            self.p2.terminate()
            self.controller.show_frame(AdminPage)
            self.startButton.config(state='normal')

    def rfid_multiprocessing(self, queue):

        while True:
            result = rd.test_commit(lecture_id)
            try:
                pass
                queue.put(result[RFID_SERIALNO])

            except:
                pass

    def scard_multiprocessing(self, queue):

        while True:
            result = ed.sc_test_commit(lecture_id)

            try:
                pass
                queue.put(result[EID_IDCODE])

            except:
                pass

q = Queue()

app = Registrator()
app.mainloop()
