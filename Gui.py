import Tkinter as Tk
import time
import MFRC522
from Database import *

# style args
font = 'verdana 15 bold'
largeFont = 'verdana 25 bold'

# custom widgets
class MyLabel(Tk.Frame) :
    def __init__(self , parent , *args , **kwargs) :
        Tk.Frame.__init__(self , parent , *args , **kwargs)
        self.label = Tk.Label(self , borderwidth = 4 , font = font)
        self.pack_propagate(0)
        self.label.pack(fill = 'both' , expand = 1)


class MyScrollBar(Tk.Frame) :
    def __init__(self , parent , *args , **kwargs) :
        Tk.Frame.__init__(self , parent , *args , **kwargs)
        self.scrollBar = Tk.Scrollbar(self )
        self.pack_propagate(0)
        self.scrollBar.pack(fill = 'both' , expand = 1)

#TODO: figure out why the scanner freezes ... read Read.py in MFRC522 class folder
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

                else :
                    self.label.configure(text = 'Please Scan New Admin Card' , bg = 'red')
                    self.after(150,self.createAdmin)

            else :
                self.label.configure(text = 'Please Scan New Admin Card' , bg = 'red')
                self.after(150 , self.createAdmin)


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

                    if emp.name == 'admin':
                        self.label.config(text = "Admin Card Read" , bg = 'green')
                        self.label.bind('<1>' , lambda x : self.adminfunc())
                        self.after(3000 , self.tick)

                    else:
                        self.label.config(text = emp.name , bg = 'green')
                        self.label.bind('<1>' , lambda x: self.function(self.uid))
                        self.after(3000, self.tick)

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
        self.label.config(text = str(temp[3]).zfill(2) + ':' + str(temp[4]).zfill(2) + ':' + str(temp[5]).zfill(2))
        # calls itself every so many milliseconds
        self.after(300 , self.tick)


class HoursLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None


    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.config(text = round((self.emp.hours + ((datetime.datetime.now() - self.emp.lastTime).seconds)) / 3600.0 , 2))

        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime

            if temp2 <= temp :
                self.label.config(text = round((self.emp.hours + (datetime.datetime.now() - self.emp.lastTime).seconds) / 3600.0 , 2))

            else :
                self.label.config(text = round((self.emp.hours + temp.seconds) / 3600.0 , 2))

        self.after(300 , self.tick)


class TotalHoursLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None


    def tick(self) :
        self.emp = employee(self.emp.uid)
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.config(text = round((self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).seconds - self.emp.overtime) / 3600.0 , 2))

        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :
                self.label.config(text = round((self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).seconds - self.emp.overtime) / 3600.0 , 2))

            else :
                self.label.config(text = round((self.emp.totalHours + temp.seconds - self.emp.overtime) / 3600.0 , 2))

        else :
            self.label.configure(text = round((self.emp.totalHours - self.emp.overtime) / 3600.0 , 2))

        self.after(300 , self.tick)


class OverHoursLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None


    def tick(self) :
        self.emp = employee(self.emp.uid)
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            if self.emp.hours > self.emp.over.seconds :
                self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds) / 3600.0 , 2))

            if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds) / 3600.0 , 2))

        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :

                if self.emp.hours > self.emp.over.seconds :
                    self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds) / 3600.0 , 2))

                if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                    self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).seconds) / 3600.0 , 2))

            else :
                if self.emp.hours > self.emp.over.seconds :
                    self.label.config(text = round((self.emp.overtime + temp.seconds) / 3600.0 , 2))

                if self.emp.totalHours > (self.emp.overweek.seconds + self.emp.overtime) :
                    self.label.config(text = round((self.emp.overtime + temp.seconds) / 3600.0 , 2))
        else :
            self.label.configure(text = round(self.emp.overtime / 3600.0 , 2))

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
        self.alertFunction = None
        self.thirtyMin = datetime.timedelta(0,1800)


    def tick(self) :
        now = datetime.datetime.now()
        if self.emp.onLunch  and (now - self.emp.lastTime).seconds >= self.thirtyMin.seconds:
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.endLunch())

        elif self.emp.onLunch  and (now - self.emp.lastTime).seconds < self.thirtyMin.seconds:
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.bind('<1>' , lambda x : self.alertFunction())

        else :
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.unbind('<1>')

        self.after(300 , self.tick)


class MyButton(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.label.configure(bg = 'blue' , relief = "groove")


class ProgramingButton(MyLabel) :

    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.name = None
        self.uid = None
        self.mLabel = None
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

                try :
                    emp = employee(self.uid)
                    self.mLabel.label.configure(text = '!!!Card alredy in Use!!!')
                    self.label.configure(bg = 'green' , relief = "groove" , text = '!?!CLEAR OLD WORKER!?!')
                    self.label.bind('<1>' , lambda x : (
                    emp.destroy() , employee.newEmployee(self.name , self.uid) , self.master.destroy()))

                except :
                    employee.newEmployee(self.name , self.uid)
                    self.label.configure(bg = 'green' , relief = "groove" , text = 'Complete!')
                    self.label.bind('<1>' , lambda x : self.master.destroy())

            else :
                self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
                self.label.unbind('<1>')
                self.after(300 , self.tick)

        else :
            self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
            self.label.unbind('<1>')
            self.after(300 , self.tick)


class ReplaceCardButton(MyLabel):
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None
        self.uid = None
        self.mLabel = None
        self.reader = MFRC522.MFRC522()

    def updateEmployee(self):
        for row  in Log.getEmployee(self.emp.uid):
            entry = Log(row[0])
            entry.uid = self.uid
            entry.update()
        self.emp.uid = self.uid
        self.emp.updateDB()




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

                try:
                    emp = employee(self.uid)
                    self.mLabel.label.configure(text = '!!!Card alredy in Use By ' + emp.name + '!!!')
                    self.label.configure(bg = 'green' , relief = "groove" , text = '!?!DELETE OLD WORKER!?!')
                    self.label.bind('<1>' , lambda x : ( emp.destroy() , self.updateEmployee() , self.master.destroy()))

                except:
                    self.label.configure(bg = 'green' , relief = "groove" , text = 'Finish!')
                    self.updateEmployee()
                    self.label.bind('<1>' , lambda x : self.master.destroy())

            else:
                self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
                self.label.unbind('<1>')
                self.after(300 , self.tick)

        else:
            self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
            self.label.unbind('<1>')
            self.after(300 , self.tick)




