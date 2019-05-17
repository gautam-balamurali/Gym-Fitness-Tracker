from tkinter import * #GUI package
import tkinter as tk
import sqlite3 as sq #For tables and database
import datetime

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', textvariable='enter'):
        super().__init__(master, textvariable=textvariable)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

global MAINID

window = Tk()
window.title("ASD LAB PROJECT")
window.geometry('800x600+0+0')
header = Label(window, text="Gym Fitness Tracker", font=("arial",30,"bold"), fg="steelblue")
header.pack(ipady=50)

con = sq.connect('Gym.db') #dB browser for sqlite needed
c = con.cursor() #SQLite command, to connect to db so 'execute' method can be called

L2 = Label(window, text = "Date", font=("arial",18)).place(x=10,y=150)
L5 = Label(window, text = "Max Weight (KG)", font=("arial",18)).place(x=10,y=200)
L6 = Label(window, text = "Reps", font=("arial",18)).place(x=10,y=250)
L7 = Label(window, text = "Category", font=("arial", 18)).place(x=10,y=300)

#Create variables for each list
comp = StringVar(window)#For 1st dd
comp.set('----') #Inital placeholder for field

comp = StringVar(window)#2nd dropdown list
comp.set('----')

day = StringVar(window)
month = StringVar(window)
year = StringVar(window)
weight = StringVar(window)
reps = StringVar(window)

#Dictionary for drop down list x2
compound = {'Bench', 'Squat', 'Deadlift','OVH'}
compd = OptionMenu(window, comp, *compound).place(x=220,y=305)
#compase = OptionMenu(window, comp, *compound).place(x=100,y=500)

#ENTRY VALUE CONFIG!
now = datetime.datetime.now()
dayT = EntryWithPlaceholder(window, textvariable=day, placeholder=now.day)
dayT.config(width=5)
dayT.place(x=220,y=155)
monthT = EntryWithPlaceholder(window, textvariable=month, placeholder=now.month)
monthT.config(width=5)
monthT.place(x=278,y=155)
yearT = EntryWithPlaceholder(window, textvariable=year, placeholder=now.year)
yearT.config(width=5)
yearT.place(x=336,y=155)
weightT = EntryWithPlaceholder(window, textvariable=weight, placeholder="100")
weightT.config(width=18)
weightT.place(x=220,y=205)
repT = EntryWithPlaceholder(window, textvariable=reps, placeholder="10")
repT.config(width=18)
repT.place(x=220,y=255)

def set_vals(*args):
    comp.set(args[0])
    day.set(args[1])
    month.set(args[2])
    year.set(args[3])
    weight.set(args[4])
    reps.set(args[5])

def clear():
    set_vals('----', '', '', '' ,'', '')

#get func to isolate the text entered in the entry boxes and submit to database
def get():
    print("You have submitted a record")

    c.execute('CREATE TABLE IF NOT EXISTS ' +comp.get()+ ' (Id INTEGER PRIMARY KEY AUTOINCREMENT, Datestamp TEXT, MaxWeight INTEGER, Reps INTEGER)') #SQL syntax

    date = datetime.date(int(year.get()),int(month.get()), int(day.get())) #Date in format from 'import datetime'

    c.execute('INSERT INTO '+comp.get()+' (Datestamp, MaxWeight, Reps) VALUES (?, ?, ?)',(date, weight.get(), reps.get())) #Insert record into database.
    con.commit()
    clear()

#Clear boxes when submit button is hit

def delete():
	c.execute('delete from '+comp.get()+' where Id in (select max(id) from '+comp.get()+')')
	con.commit()

def update():
	c.execute('select * from '+comp.get())
	data = list(c)[0]
	date = data[1].split('-')
	set_vals(comp.get(), date[2], date[1], date[0], data[2], data[3])
	delete()
	con.commit()

def record():
    c.execute('SELECT * FROM ' +comp.get()) #Select from which ever compound lift is selected

    frame = Frame(window)
    frame.place(x= 500, y = 150)

    Lb = Listbox(frame, height = 13, width = 35,font=("arial", 15))
    Lb.pack(side = LEFT, fill = Y)

    scroll = Scrollbar(frame, orient = VERTICAL) # set scrollbar to list box for when entries exceed size of list box
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set)

#    Lb.insert(0, 'Date, Max Weight, Reps') #first row in listbox

    data = c.fetchall() # Gets the data from the table

    for row in data:
        nrow = "{0:10} : {1:<4s}x {2:<4s}kg".format(str(row[1]), str(row[3]), str(row[2]))
        Lb.insert(1,nrow) # Inserts record row by row in list box

    L7 = Label(window, text = comp.get()+ ' Workouts : In order of entry',
               font=("arial", 16)).place(x=500,y=100) # Title of list box, given which compound lift is chosen
    con.commit()

button_1 = Button(window, text="Submit",command=get)
button_1.place(x=150,y=400)
button_1.config(width=10)

button_2 = Button(window,text= "Clear",command=clear)
button_2.place(x=10,y=400)
button_2.config(width=10)

button_3 = Button(window,text="Open DB",command=record)
button_3.place(x=290,y=435)
button_3.config(width=10)

button_1 = Button(window, text="Delete Last",command=delete)
button_1.place(x=150,y=435)
button_1.config(width=10)

button_5 = Button(window,text="Quit",command=window.destroy)
button_5.place(x=10,y=470)
button_5.config(width=10)

button_4 = Button(window,text="Update Last",command=update)
button_4.place(x=10,y=435)
button_4.config(width=10)

window.mainloop() #mainloop() -> make sure that window stays open
