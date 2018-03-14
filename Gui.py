import Tkinter as Tk
import time
import RPi.GPIO as GPIO
import MFRC522
from Database import *

#bug fixes
GPIO.setwarnings(False)

# style args
font = 'verdana 15 bold'

# custom widgets

class MyLabel(Tk.Frame) :

    def __init__(self , parent , *args , **kwargs) :
        Tk.Frame.__init__(self , parent , *args , **kwargs)
        self.label = Tk.Label(self , borderwidth = 4 , font = font)
        self.pack_propagate(0)
        self.label.pack(fill = 'both' , expand = 1)


class ScanLabel(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.uid = None
        self.cardRead = 0
        self.reader = MFRC522.MFRC522()
        self.function = None
        self.adminfunc = None
        self.createAdmin()

    def createAdmin(self) :
        temp = dbi('SELECT uid FROM employees WHERE name = "admin"')
        try :
            temp.fetchall()[0][0]
        except :
            # Scan for cards
            (status , TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            # If a card is found
            if status == self.reader.MI_OK :
                # Get the UID of the card
                (status , uid) = self.reader.MFRC522_Anticoll()
                # If we have the UID, continue
                if status == self.reader.MI_OK :
                    uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    employee.newEmployee('admin' , uid)
                    GPIO.cleanup()
                else :
                    self.label.configure(text = 'Please Scan New Admin Card' , bg = 'red')
                    createAdmin()
                    time.sleep(1)
            else :
                self.label.configure(text = 'Please Scan New Admin Card' , bg = 'red')
                createAdmin()
                time.sleep(1)

    def tick(self) :
        # Scan for cards
        status = None
        (status , TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            # If a card is found
        if status == self.reader.MI_OK :
            # Get the UID of the card
            (status , uid) = self.reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == self.reader.MI_OK :
                self.uid = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
                try:
                    emp = employee(self.uid)
                    print(emp.name)
                    if emp.name == 'admin':
                        self.label.config(text = "Admin Card Read" , bg = 'green')
                        self.label.bind('<1>' , lambda x : self.adminfunc())
                        self.after(5000 , self.tick)
                    else:
                        self.label.config(text = emp.name , bg = 'green')
                        self.label.bind('<1>' , lambda x: self.function(self.uid))
                        self.after(5000, self.tick)
                except:
                    self.tick()
        else:
            self.after(300 , self.tick)
            self.label.unbind('<1>')
            self.label.configure(text = 'Please Scan Card' , bg = 'red')


class TimeLabel(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.label.config(text = time.localtime() , relief = "ridge")
        self.tick()

    def tick(self) :
        # get the current local time from the PC
        temp = time.localtime()
        self.label.config(text = str(temp[3] % 12) + ':' + str(temp[4]).zfill(2) + ':' + str(temp[5]).zfill(2))
        # calls itself every so many milliseconds
        self.after(300 , self.tick)


class HoursLabel(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.config(
                text = datetime.timedelta(0 , (self.emp.hours + (datetime.datetime.now() - self.emp.lastTime).seconds)))
        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :
                self.label.config(text = datetime.timedelta(0 , (
                        self.emp.hours + (datetime.datetime.now() - self.emp.lastTime).seconds)))
            else :
                self.label.config(text = datetime.timedelta(0 , (self.emp.hours + temp.seconds)))

        self.after(300 , self.tick)


class TotalHoursLabel(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.config(text = datetime.timedelta(0 , (
                    self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).seconds)))
        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :
                self.label.config(text = datetime.timedelta(0 , (
                        self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).seconds)))
            else :
                self.label.config(text = datetime.timedelta(0 , (self.emp.totalHours + temp.seconds)))
        self.after(300 , self.tick)


class OverHoursLabel(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            if self.emp.hours > self.emp.over.seconds :
                self.label.config(text = datetime.timedelta(0 , (
                        self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds)))
            if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                self.label.config(text = datetime.timedelta(0 , (
                        self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds)))
        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :
                if self.emp.hours > self.emp.over.seconds :
                    self.label.config(text = datetime.timedelta(0 , (
                            self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds)))
                if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                    self.label.config(text = datetime.timedelta(0 , (
                            self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds)))
            else :
                if self.emp.hours > self.emp.over.seconds :
                    self.label.config(text = datetime.timedelta(0 , (self.emp.overtime + temp.seconds)))
                if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                    self.label.config(text = datetime.timedelta(0 , (self.emp.overtime + temp.seconds)))
        self.after(300 , self.tick)


class ClockInButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if not self.emp.clockedIn :
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.clockIn())
        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')
        self.after(300 , self.tick)


class ClockOutButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.clockOut())
        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')
        self.after(300 , self.tick)


class TakeTenButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.startTen())
        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')
        self.after(300 , self.tick)


class EndTenButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.onTen :
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.endTen())
        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')
        self.after(300 , self.tick)


class TakeLunchButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.startLunch())
        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')
        self.after(300 , self.tick)


class EndLunchButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None

    def tick(self) :
        if self.emp.onLunch :
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.endLunch())
        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')
        self.after(300 , self.tick)

class BlueButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.label.configure(bg = 'blue' , relief = "groove")

class ProgramingButton(MyLabel):
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.name = None
        self.uid = None
        self.reader = MFRC522.MFRC522()

    def tick(self) :
        # Scan for cards
        (status , TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
        # If a card is found
        if status == self.reader.MI_OK :
            # Get the UID of the card
            (status , uid) = self.reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == self.reader.MI_OK :
                self.uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                employee.newEmployee(self.name , self.uid)
                GPIO.cleanup()
                self.label.configure(bg = 'green' , relief = "groove" , text = 'Complete!')
                self.label.bind('<1>' , lambda x : t.destroy)
            else:
                self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
                self.label.unbind('<1>')
                self.after(300 , self.tick)
        else:
            self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
            self.label.unbind('<1>')
            self.after(300 , self.tick)
