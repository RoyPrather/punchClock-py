import Tkinter as Tk
import time
import datetime


#style args

# custom widgets

class MyLabel(Tk.Frame):
    def __init__(self , parent , *args , **kwargs) :
        Tk.Frame.__init__(self , parent , *args , **kwargs)
        self.label = Tk.Label(self)
        self.pack_propagate(0)
        self.label.pack(fill = 'both' , expand = 1)


class TimeLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.label.config(text = time.localtime())
        self.tick()

    def tick(self) :
        # get the current local time from the PC
        temp = time.localtime()
        self.label.config(text = str(temp[3] % 12) + ':' + str(temp[4]).zfill(2) + ':' + str(temp[5]).zfill(2))
        # calls itself every so many milliseconds
        self.after(300 , self.tick)

class HoursLabel(MyLabel) :

    def __init__(self , parent  , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) :
            self.label.config(text =datetime.timedelta(0,(self.emp.hours + (datetime.datetime.now() - self.emp.lastTime).seconds)))
        self.after(300 , self.tick)

class TotalHoursLabel(MyLabel) :

    def __init__(self , parent  , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) :
            self.label.config(text =datetime.timedelta(0,(self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).seconds)))
        self.after(300 , self.tick)

class OverHoursLabel(MyLabel) :

    def __init__(self , parent  , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) :
            if self.emp.hours > self.emp.over.seconds :
                self.label.config(text =datetime.timedelta(0,(self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds)))
            if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                self.label.config(text =datetime.timedelta(0,(self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds)))
        self.after(300 , self.tick)

class ClockInButton(MyLabel) :

    def __init__(self , parent  , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None
        self.tick

    def tick(self):
        if not self.emp.clockedIn:
            self.label.configure(bg = 'green')
            self.label.bind('<1>' , lambda x: self.emp.clockIn())
        else:
            self.label.configure(bg = 'red')
            self.label.unbind('<1>')
        self.after(300 , self.tick)

class ClockOutButton(MyLabel) :

    def __init__(self , parent  , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None
        self.tick

    def tick(self):
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen):
            self.label.configure(bg = 'green')
            self.label.bind('<1>' , lambda x: self.emp.clockOut())
        else:
            self.label.configure(bg = 'red')
            self.label.unbind('<1>')
        self.after(300 , self.tick)