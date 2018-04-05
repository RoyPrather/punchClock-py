import Tkinter as Tk
import time
import MFRC522
from Database import *
reader = MFRC522.MFRC522()

scanToggle = 1

def toggleOn(Toggle):
    Toggle = 1

def toggleOff(Toggle):
    Toggle = 0

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

class RunningHoursListbox(Tk.Listbox):
    def __init__(self , parent , *args , **kwargs) :
        Tk.Listbox.__init__(self , parent , *args , **kwargs)
        self.emps = []
        self.tick()

    def tick(self):
        count = 0
        self.emps = []
        self.delete(0,'end')
        for uid in employee.listEmployees():
            emp = employee(uid[0])
            if emp.name != 'admin':
                if emp.clockedIn and (not emp.onLunch) and (not emp.onTen) :
                    self.emps.insert(count , emp)
                    self.insert(count , '{0:>20}{1:>15}{2:>15}'.format(emp.name ,
                                             'Hours: ' + str(round((emp.totalHours + (datetime.datetime.now() - emp.lastTime).total_seconds() - emp.overtime) / 3600.0 , 2)) ,
                                             'Overtime: ' + str(round(emp.overtime / 3600.0 , 2))))

                elif emp.onTen :
                    temp = datetime.timedelta(0 , 600)
                    temp2 = datetime.datetime.now() - emp.lastTime

                    if temp2 <= temp :
                        self.emps.insert(count , emp)
                        self.insert(count , '{0:>20}{1:>15}{2:>15}'.format(emp.name ,
                                                 'Hours: ' + str(round((emp.totalHours + (datetime.datetime.now() - emp.lastTime).total_seconds() - emp.overtime)   / 3600.0, 2)),
                                                 'Overtime: ' + str(round(emp.overtime / 3600.0 , 2))))

                    else :
                        self.emps.insert(count , emp)
                        self.insert(count , '{0:>20}{1:>15}{2:>15}'.format(emp.name ,
                                                 'Hours: ' + str(round((emp.totalHours + temp.total_seconds() - emp.overtime) / 3600.0 , 2)),
                                                 'Overtime: ' + str(round(emp.overtime / 3600.0 , 2))))

                else:
                    self.emps.insert(count , emp)
                    self.insert(count , '{0:>20}{1:>15}{2:>15}'.format(emp.name ,
                                             'Hours: ' + str(round((emp.totalHours - emp.overtime) / 3600.0 , 2)) ,
                                             'Overtime: ' + str(round(emp.overtime / 3600.0 , 2))))
                count += 1
        self.after(15000 , self.tick)


class ScanLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.uid = None
        self.function = None
        self.adminfunc = None
        toggleOn(scanToggle)

    def startUp(self):
        temp = dbi('SELECT uid FROM employees WHERE name = "admin"')
        try :
            temp.fetchall()[0][0]
            self.tick()
        except :
            self.createAdmin()


    def createAdmin(self) :
        # Scan for cards
        (status , TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        # If a card is found
        if status == reader.MI_OK :
            # Get the UID of the card
            (status , uid) = reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == reader.MI_OK :
                uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                employee.newEmployee('admin' , uid)
                self.tick()

            else :
                self.label.configure(text = 'Please Scan New Admin Card' , bg = 'red')
                self.after(150,self.createAdmin)

        else :
            self.label.configure(text = 'Please Scan New Admin Card' , bg = 'red')
            self.after(150 , self.createAdmin)


    def tick(self) :
        if scanToggle:
            # Scan for cards
            (status , TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            # If a card is found
            if status == reader.MI_OK :
                # Get the UID of the card
                (status , uid) = reader.MFRC522_Anticoll()
                # If we have the UID, continue
                if status == reader.MI_OK :
                    self.uid = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
                    try:
                        emp = employee(self.uid)
                        if emp.name == 'admin':
                            self.label.config(text = "Admin Card Read" , bg = 'green')
                            self.label.bind('<1>' , lambda x : (toggleOff(scanToggle) , self.adminfunc()))
                            self.after(3000 , self.tick)

                        else:
                            self.label.config(text = emp.name , bg = 'green')
                            self.label.bind('<1>' , lambda x:(toggleOff(scanToggle) , self.function(self.uid)))
                            self.after(3000, self.tick)

                    except:
                        self.after(300 , self.tick)

                else :
                    self.after(300 , self.tick)
                    self.label.unbind('<1>')
                    self.label.configure(text = 'Please Scan Card' , bg = 'red')

            else:
                self.after(300 , self.tick)
                self.label.unbind('<1>')
                self.label.configure(text = 'Please Scan Card' , bg = 'red')

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
            self.label.config(text = datetime.timedelta(0 ,self.emp.hours + (datetime.datetime.now() - self.emp.lastTime).total_seconds()))

        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime

            if temp2 <= temp :
                self.label.config(text = datetime.timedelta(0 , self.emp.hours + (datetime.datetime.now() - self.emp.lastTime).total_seconds()))

            else :
                self.label.config(text =datetime.timedelta(0 , self.emp.hours + temp.total_seconds()))

        self.after(300 , self.tick)


class TotalHoursLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None


    def tick(self) :
        self.emp = employee(self.emp.uid)
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            self.label.config(text = round((self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).total_seconds() - self.emp.overtime) / 3600.0 , 2))

        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :
                self.label.config(text = round((self.emp.totalHours + (datetime.datetime.now() - self.emp.lastTime).total_seconds() - self.emp.overtime) / 3600.0 , 2))

            else :
                self.label.config(text = round((self.emp.totalHours + temp.total_seconds() - self.emp.overtime) / 3600.0 , 2))

        else :
            self.label.configure(text = round((self.emp.totalHours - self.emp.overtime) / 3600.0 , 2))

        self.after(300 , self.tick)


class OverHoursLabel(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None


    def tick(self) :
        if self.emp.clockedIn and (not self.emp.onLunch) and (not self.emp.onTen) :
            if self.emp.hours > self.emp.over.total_seconds() :
                self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).total_seconds()) / 3600.0 , 2))

            elif self.emp.totalHours > (self.emp.overweek.total_seconds() + self.emp.overtime) :
                self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).total_seconds()) / 3600.0 , 2))

            else:
                self.label.configure(text = round(self.emp.overtime / 3600.0 , 2))

        elif self.emp.onTen :
            temp = datetime.timedelta(0 , 600)
            temp2 = datetime.datetime.now() - self.emp.lastTime
            if temp2 <= temp :

                if self.emp.hours > self.emp.over.total_seconds() :
                    self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).total_seconds()) / 3600.0 , 2))

                elif self.emp.totalHours > (self.emp.overweek.total_seconds() + self.emp.overtime) :
                    self.label.config(text = round((self.emp.overtime + (datetime.datetime.now() - self.emp.lastTime).total_seconds()) / 3600.0 , 2))

                else:
                    self.label.configure(text = round(self.emp.overtime / 3600.0 , 2))


            else :
                if self.emp.hours > self.emp.over.total_seconds() :
                    self.label.config(text = round((self.emp.overtime + temp.total_seconds()) / 3600.0 , 2))

                if self.emp.totalHours > (self.emp.overweek.total_seconds() + self.emp.overtime) :
                    self.label.config(text = round((self.emp.overtime + temp.total_seconds()) / 3600.0 , 2))
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
        if self.emp.onLunch  and (now - self.emp.lastTime).total_seconds() >= self.thirtyMin.total_seconds():
            self.label.configure(bg = 'green' , relief = "groove")
            self.label.bind('<1>' , lambda x : self.emp.endLunch())

        elif self.emp.onLunch  and (now - self.emp.lastTime).total_seconds() < self.thirtyMin.total_seconds():
            self.label.configure(bg = 'red' , relief = "ridge")
            self.label.bind('<1>' , lambda x : self.alertFunction(self.emp))

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
        self.delConfirm = None

    def tick(self) :
        # Scan for cards
        (status , TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        # If a card is found
        if status == reader.MI_OK :
            # Get the UID of the card
            (status , uid) = reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == reader.MI_OK :
                self.uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                try :
                    emp = employee(self.uid)
                    self.mLabel.label.configure(text = '!!!Card alredy in Use By ' + emp.name + '!!!')
                    self.label.configure(bg = 'green' , relief = "groove" , text = '!?!DELETE OLD WORKER!?!')
                    self.label.bind('<1>' , lambda x : (self.delConfirm(emp , self.name) , self.master.destroy()))

                except :
                    employee.newEmployee(self.name , self.uid)
                    self.label.configure(bg = 'green' , relief = "groove" , text = 'Complete!')
                    self.label.bind('<1>' , lambda x : (self.master.destroy()))

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
        self.delConfirm = None


    def tick(self) :
        # Scan for cards
        (status , TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        # If a card is found
        if status == reader.MI_OK :
            # Get the UID of the card
            (status , uid) = reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == reader.MI_OK :
                self.uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                try:
                    emp = employee(self.uid)
                    self.mLabel.label.configure(text = '!!!Card alredy in Use By ' + emp.name + '!!!')
                    self.label.configure(bg = 'green' , relief = "groove" , text = '!?!DELETE OLD WORKER!?!')
                    self.label.bind('<1>' , lambda x : (self.delConfirm(emp ,self.emp) , self.master.destroy()))

                except:
                    self.label.configure(bg = 'green' , relief = "groove" , text = 'Finish!')
                    self.emp.replaceCard(self.uid)
                    self.label.bind('<1>' , lambda x : (self.master.destroy()))

            else:
                self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
                self.label.unbind('<1>')
                self.after(300 , self.tick)

        else:
            self.label.configure(bg = 'red' , relief = "ridge" , text = 'Please Wait')
            self.label.unbind('<1>')
            self.after(300 , self.tick)


class LunchOverrideButton(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.emp = None
        self.mLabel = None

    def tick(self) :
        # Scan for cards
        (status , TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        # If a card is found
        if status == reader.MI_OK :
            # Get the UID of the card
            (status , uid) = reader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == reader.MI_OK :
                UID = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                try :
                    admin = employee(UID)
                    if admin.name == 'admin':
                        self.mLabel.label.configure(text = '!!!This May Not Be Legal!!!')
                        self.label.configure(bg = 'green' , relief = "groove" , text = '!?!End Lunch Early!?!')
                        self.label.bind('<1>' , lambda x: (self.emp.endLunch() , self.master.destroy()))
                    else:
                        self.label.configure(bg = 'red' , relief = "ridge" , text = 'Manager Override')
                        self.label.unbind('<1>')
                        self.after(300 , self.tick)

                except :
                    self.label.configure(bg = 'red' , relief = "ridge" , text = 'Manager Override')
                    self.label.unbind('<1>')
                    self.after(300 , self.tick)

            else :
                self.label.configure(bg = 'red' , relief = "ridge" , text = 'Manager Override')
                self.label.unbind('<1>')
                self.after(300 , self.tick)

        else :
            self.label.configure(bg = 'red' , relief = "ridge" , text = 'Manager Override')
            self.label.unbind('<1>')
            self.after(300 , self.tick)


class AutoDestroyButton(MyLabel) :
    def __init__(self , parent , *args , **kwargs) :
        MyLabel.__init__(self , parent , *args , **kwargs)
        self.label.configure(bg = 'blue' , relief = "groove")
        self.stime = datetime.datetime.now()
        self.tick()

    def tick(self):
        if (datetime.datetime.now() - self.stime) > datetime.timedelta(0,60):
            self.master.destroy()
        else:
            self.after(1000, self.tick)


class AlertListbox(Tk.Listbox):
    def __init__(self , parent , *args , **kwargs) :
        Tk.Listbox.__init__(self , parent , *args , **kwargs)
        self.tick()

    def tick(self):
        self.delete(0,'end')
        for uid in employee.listEmployees():
            emp = employee(uid[0])
            if emp.name != 'admin':
                if emp.onTen:
                    self.insert('end' , '{0:<20}{1:<15}'.format(emp.name , 'On Ten'))

                elif emp.onLunch:
                    self.insert('end' , '{0:<20}{1:<15}'.format(emp.name , 'On Lunch'))

                elif emp.clockedIn:
                   self.insert('end' , '{0:<20}{1:<15}'.format(emp.name , 'Clocked In'))

                if emp.clockedIn and (not emp.onLunch):
                    if ((datetime.datetime.now() - emp.lastTime).total_seconds() >= datetime.timedelta(0,0,0,0,50,1).total_seconds()):
                        self.insert('end', 'Needs A Break Soon')

                    if (emp.hours + (datetime.datetime.now() - emp.lastTime).total_seconds() > datetime.timedelta(0,0,0,0,0,4).total_seconds()) and not emp.tookLunch:
                        if (emp.hours + (datetime.datetime.now() - emp.lastTime).total_seconds() > datetime.timedelta(0,0,0,0,0,6).total_seconds()):
                            self.insert('end' , 'Working Illegaly')

                        elif (emp.hours + (datetime.datetime.now() - emp.lastTime).total_seconds() > datetime.timedelta(0,0,0,0,0,5).total_seconds()):
                            clockOutTime = datetime.datetime.now() + datetime.timedelta(0,0,0,0,0,6) - datetime.timedelta(0,emp.hours + (datetime.datetime.now() - emp.lastTime).total_seconds())
                            self.insert('end' , 'Needs To Leave By ' + str(clockOutTime.hour) + ':' + str(clockOutTime.minute))

                        else:
                            lunchTime = datetime.datetime.now() + datetime.timedelta(0,0,0,0,0,5) - datetime.timedelta(0,emp.hours + (datetime.datetime.now() - emp.lastTime).total_seconds())
                            self.insert('end' , 'Needs Lunch By ' + str(lunchTime.hour) + ':' + str(lunchTime.minute))

        self.after(3000 , self.tick)



