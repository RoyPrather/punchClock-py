from Gui import *

# create main window
root = Tk.Tk()
root.attributes('-fullscreen' , True)
root.lift()
root.focus_force()

#crate sizing variables
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

def setWidth(percent):
    return((screenWidth / 100) * percent)


def setHeight(percent):
    return((screenHeight / 100) * percent)


# Bring up Clock in Screen
def clockInWin(id) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create employee class instance
    emp = employee(id)

    # create widgets
    nameLabel = MyLabel(t ,  width = setWidth(50) , height = setHeight(18))
    hoursTitle = MyLabel(t , width = setWidth(50) , height = setHeight(12))
    hoursTotal = TotalHoursLabel(t , width = setWidth(50) , height = setHeight(12))
    todayTitle = MyLabel(t , width = setWidth(50) , height = setHeight(12))
    todayHours = HoursLabel(t , width = setWidth(50) , height = setHeight(12))
    overTitle = MyLabel(t , width = setWidth(50) , height = setHeight(12))
    overHours = OverHoursLabel(t , width = setWidth(50) , height = setHeight(12))
    placeHolder1 = MyLabel(t , width = setWidth(50) , height = setHeight(12))
    placeHolder2 = MyLabel(t , width = setWidth(50) , height = setHeight(12))

    clockInButton = ClockInButton(t , width = setWidth(50) , height = setHeight(12))
    clockOutButton = ClockOutButton(t , width = setWidth(50) , height = setHeight(12))
    tenMinOutButton = TakeTenButton(t , width = setWidth(50) , height = setHeight(12))
    tenMinInButton = EndTenButton(t , width = setWidth(50) , height = setHeight(12))
    lunchOutButton = TakeLunchButton(t , width = setWidth(50) , height = setHeight(12))
    lunchInButton = EndLunchButton(t , width = setWidth(50) , height = setHeight(12))
    sendMessageButton = BlueButton(t , width = setWidth(50) , height = setHeight(12))
    backButton = BlueButton(t , width = setWidth(50) , height = setHeight(12))

    # configure widgets
    nameLabel.label.config(text = emp.name)
    hoursTitle.label.config(text = 'Total Hours This Period')
    hoursTotal.label.config(text = datetime.timedelta(0 , emp.totalHours))
    hoursTotal.emp = emp
    hoursTotal.tick()
    todayTitle.label.config(text = 'Hours Worked This Shift')
    todayHours.label.config(text = datetime.timedelta(0 , emp.hours))
    todayHours.emp = emp
    todayHours.tick()
    overTitle.label.config(text = 'Over Time')
    overHours.label.config(text = datetime.timedelta(0 , emp.overtime))

    clockInButton.label.configure(text = 'Clock In')
    clockInButton.emp = emp
    clockInButton.tick()
    clockOutButton.label.configure(text = 'Clock Out')
    clockOutButton.emp = emp
    clockOutButton.tick()
    tenMinOutButton.label.configure(text = 'Take 10 Minute Break')
    tenMinOutButton.emp = emp
    tenMinOutButton.tick()
    tenMinInButton.label.configure(text = 'Return From 10 Minute Break')
    tenMinInButton.emp = emp
    tenMinInButton.tick()
    lunchOutButton.label.configure(text = 'Take Lunch Break')
    lunchOutButton.emp = emp
    lunchOutButton.tick()
    lunchInButton.label.configure(text = 'Return Lunch Break')
    lunchInButton.emp = emp
    lunchInButton.tick()
    sendMessageButton.label.configure(text = 'Message Management')
    backButton.label.configure(text = 'Done')

    # place widgets in window
    nameLabel.grid(column = 0 , row = 0 , columnspan = 2)
    hoursTitle.grid(column = 0 , row = 1)
    hoursTotal.grid(column = 0 , row = 2)
    todayTitle.grid(column = 0 , row = 3)
    todayHours.grid(column = 0 , row = 4)
    overTitle.grid(column = 0 , row = 5)
    overHours.grid(column = 0 , row = 6)
    placeHolder1.grid(column = 0 , row = 7)
    sendMessageButton.grid(column = 0 , row = 8)

    clockInButton.grid(column = 1 , row = 1)
    tenMinOutButton.grid(column = 1 , row = 2)
    tenMinInButton.grid(column = 1 , row = 3)
    lunchOutButton.grid(column = 1 , row = 4)
    lunchInButton.grid(column = 1 , row = 5)
    clockOutButton.grid(column = 1 , row = 6)
    placeHolder2.grid(column = 1 , row = 7)
    backButton.grid(column = 1 , row = 8)

    # bind widgets
    sendMessageButton.label.bind('<1>' , lambda x: sendMessageWin(emp.name))
    backButton.label.bind('<1>' , lambda x: t.destroy())


# Bring up  admin screen
def adminWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()
    # create widgets
    viewMessageButton = BlueButton(t , width = setWidth(50) , height = setHeight(30))
    viewLogButton = BlueButton(t , width = setWidth(50) , height = setHeight(30))
    newEmployeeButton = BlueButton(t , width = setWidth(50) , height = setHeight(30))
    createReportButton = BlueButton(t , width = setWidth(50) , height = setHeight(30))
    newAdminButton = BlueButton(t , width = setWidth(50) , height = setHeight(30))
    backButton = BlueButton(t , width = setWidth(50) , height = setHeight(30))
    closeButton = BlueButton(t , height = setHeight(15) , width = setWidth(25))

    #configure Widgets
    viewMessageButton.label.configure(text = 'View Messages')
    viewLogButton.label.configure(text = 'View Employee Hours')
    newEmployeeButton.label.configure(text = 'Create New Employee')
    createReportButton.label.configure(text = 'End Pay Period')
    newAdminButton.label.configure(text = 'Create New Admin Card')
    backButton.label.configure(text ='Back')
    closeButton.label.configure(text = 'Close Program')

    # place widgets in window
    viewMessageButton.grid(column = 0 , row = 0)
    viewLogButton.grid(column = 0 , row = 1)
    newEmployeeButton.grid(column = 0 , row = 2)
    createReportButton.grid(column = 1 , row = 0)
    newAdminButton.grid(column = 1 , row = 1)
    backButton.grid(column = 1 , row = 2)
    closeButton.grid(column = 0 , row = 3 , columnspan = 2)

    # bind widgets
    viewMessageButton.label.bind('<1>' , lambda x: readMessageWin())
    viewLogButton.label.bind('<1>' , lambda x: timeCardListWin())
    newEmployeeButton.label.bind('<1>' , lambda x: newEmployeeWin())
    createReportButton.label.bind('<1>' , lambda x: reportWin())
    newAdminButton.label.bind('<1>' , lambda x: programCardWin('admin'))
    backButton.label.bind('<1>' , lambda x: t.destroy())
    closeButton.label.bind('<1>' , lambda x : root.destroy())

# Bring up new employee screen
def newEmployeeWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(25))
    nameEntry = Tk.Entry(t , width = 30)
    submitButton = BlueButton(t , width = setWidth(50) , height = setHeight(25))
    backButton = BlueButton(t , width = setWidth(50) , height = setHeight(25))

    #configure widgets
    submitButton.label.configure( text = 'Create Employee')
    nameEntry.configure(font = font)
    titleLabel.label.configure(text = 'Enter New Employee Name')
    backButton.label.configure(text = 'Cancel')

    # place widgets in window
    titleLabel.grid(row = 0 , column = 0 , columnspan = 2)
    nameEntry.grid(row = 1 , column = 0 , columnspan = 2)
    nameEntry.focus()
    submitButton.grid(row = 2 , column = 1)
    backButton.grid(row = 2 , column = 0)

    # bind widgets
    submitButton.label.bind('<1>' , lambda x: (programCardWin(nameEntry.get()), t.destroy()))
    backButton.label.bind('<1>' , lambda x: t.destroy())


# Bring up new admin screen
def programCardWin(name) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    dLabel = MyLabel(t , width = setWidth(100) , height = setHeight(75))
    kButton = ProgramingButton(t , width = setWidth(50) , height = setHeight(25))
    backButton = BlueButton(t , width = setWidth(50) , height = setHeight(25))

    #configure widgets
    dLabel.label.configure(text = 'Scan New Card')
    kButton.name = name
    kButton.mLabel = dLabel
    kButton.tick()
    backButton.label.configure(text = 'Cancel')

    # place widgets in window
    dLabel.grid(row = 0 , column = 0,  columnspan = 2)
    kButton.grid(row = 1 , column = 1)
    backButton.grid(row = 1 , column = 0)

    # bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())


# Bring up hours report
def reportWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    totalLabel = Tk.Label(t , text = 'Total Hours this Period :' , width = 40)
    totalHours = Tk.Label(t , text = 'test' , width = 40)
    nameLabel = Tk.Label(t , text = 'Name' , width = 26)
    hoursLabel = Tk.Label(t , text = 'Regular Hours' , width = 26)
    overLabel = Tk.Label(t , text = 'Hours Overtime' , width = 26)
    reportFrame = Tk.Frame(t , height = 100, width = 800)
    backButton = Tk.Button(t , text = 'Cancel' , command = t.destroy, width = 80)


    # place widgets in window
    totalLabel.grid(column = 0 , row = 0 , columnspan = 2)
    totalHours.grid(column = 2 , row = 0 , columnspan = 2)
    nameLabel.grid(column = 1 , row = 1)
    hoursLabel.grid(column = 2 , row = 1)
    overLabel.grid(column = 3 , row = 1)
    reportFrame.grid(column = 0 , row =2 , columnspan = 4)
    backButton.grid(column = 0 , row = 3 , columnspan = 4)


# Bring up Messge sending window
def readMessageWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = Tk.Label(t , text = 'Message Log' , width = 80)
    messageFrame = Tk.Frame(t , width = 800 , height = 100)
    backButton = Tk.Button(t , text = 'Back' , command = t.destroy , width = 80)

    # place widgets in window
    titleLabel.grid(row = 0)
    messageFrame.grid(row = 1)
    backButton.grid(row = 2)
    # bind widgets


# Bring up Message board to view messages
def sendMessageWin(name) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()
    # create widgets
    titleLabel = Tk.Label(t , text = 'Send a Message', width = 80)
    message = ''
    messageEntry = Tk.Entry(t , textvariable = message , width = 80)
    sendButton = Tk.Button(t , text = 'Send', width = 80)
    backButton = Tk.Button(t , text = 'Cancel' , command = t.destroy, width = 80)

    # place widgets in window
    titleLabel.grid(row = 0)
    messageEntry.grid(row = 1)
    sendButton.grid(row = 2)
    backButton.grid(row = 3)
    # bind widgets


#employee list for time cards
def timeCardListWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(70))
    backButton = BlueButton(t , width = setWidth(25) , height = setHeight(15))
    submitButton = BlueButton(t , width = setWidth(25) , height = setHeight(15))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    nameFrame = Tk.Listbox(ListboxFrame , width = setWidth(75) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = 'verdana 25 bold')

    #configure widgets
    titleLabel.label.configure(text = 'Choose an Employee to Veiw')
    submitButton.label.configure(text = 'View Log')
    backButton.label.configure(text = 'Back')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = nameFrame.yview)

    #place widgets in window
    titleLabel.grid(column = 0 , row = 0 , columnspan = 2)
    ListboxFrame.grid(column = 0 , row = 1 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    nameFrame.pack(fill = 'both' , side = 'left')
    submitButton.grid(column = 1 , row = 2)
    backButton.grid(column = 0 , row = 2)

    #place list of employees into nameFrame
    count = 0
    emps = []
    for uid in employee.listEmployees():
        emp = employee(uid[0])
        if emp.name != 'admin':
            emps.insert(count , emp)
            nameFrame.insert(count , emp.name + '    ' + str(round(emp.totalHours / 360.0 , 2))  + '  Hours')
            count += 1

    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    submitButton.label.bind('<1>' , lambda x: timeCardDayWin(emps[nameFrame.curselection()[0]]))


def timeCardWin(emp , year , month , day) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    backButton = BlueButton(t , width = setWidth(25) , height = setHeight(25))
    editButton = BlueButton(t, width = setWidth(25) , height = setHeight(25))
    ListboxFrame = Tk.Frame(t, width = setWidth(100) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    LogListbox = Tk.Listbox(ListboxFrame , width = setWidth(90) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)
    hoursLabel = MyLabel(t , width = setWidth(100) , height = setHeight(10))

    #configure widgets
    titleLabel.label.configure(text = emp.name)
    backButton.label.configure(text = 'Back')
    editButton.label.configure(text = 'Edit')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = LogListbox.yview)

    #place widgets
    titleLabel.grid(row = 0 , column = 0 , columnspan = 2)
    ListboxFrame.grid(row = 1 , column = 0 , columnspan = 2)
    hoursLabel.grid(row = 2 , column = 0 , columnspan = 2)
    backButton.grid(row = 3 , column = 0)
    editButton.grid(row = 3 , column = 1)
    scrollBar.pack(fill = 'y' , side = 'right')
    LogListbox.pack(fill = 'both' , side = 'left')


    hours = 0
    for entry in log.getDay(year , month , day, emp.id):
        if entry[8] == 1:
            LogListbox.insert('end' , 'Clocked In At:                ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 2 :
            LogListbox.insert('end' , 'Started A Ten At:           ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 3 :
            LogListbox.insert('end' , 'Returned From Ten At: ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 4 :
            LogListbox.insert('end' , 'Started A Lunch At:       ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 5 :
            LogListbox.insert('end' , 'Returned From Lunch At: ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 6 :
            LogListbox.insert('end' , 'Clocked Out At:             ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 7 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 8 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 360.0 , 2)) + ' Hours')

        elif entry[8] == 9 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 360.0 , 2)) + 'Overtime Hours')

        elif entry[8] == 10 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 360.0 , 2)) + 'Overtime Hours')

        hours += entry[7]

    hoursLabel.label.configure(text ='Hours This Day  ' + str(round(hours / 360.0 , 2)))


   #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    editButton.label.bind('<1>' , lambda x: editTimeCardWin(emp))


def timeCardDayWin(emp):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    confirmButton = BlueButton(t , width = setWidth(25) , height = setHeight(25))
    backButton = BlueButton(t , width = setWidth(25) , height = setHeight(25))
    ListboxFrame = Tk.Frame(t, width = setWidth(80) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    daysListLabel = Tk.Listbox(ListboxFrame , width = 30 , yscrollcommand = scrollBar.scrollBar.set , selectmode = 'single' , font = 'verdana 25 bold')

    #configure widgets
    titleLabel.label.configure(text = 'Choose Day To Veiw')
    backButton.label.configure(text = 'Cancel')
    confirmButton.label.configure(text = 'OK')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = daysListLabel.yview)

    periodStart = log(0)
    stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
    dtime = datetime.datetime.now()
    tdelta = (dtime - stime).days + 1
    print(tdelta)
    days = []
    count = 0
    for day in range(tdelta):
        temp = dtime - datetime.timedelta(day)
        daysListLabel.insert(count, str(temp.month) +'/'+ str(temp.day) +'/'+ str(temp.year))
        days.insert(count, temp)

    #place widgets
    titleLabel.grid(column = 0 , row = 0 , columnspan = 2)
    ListboxFrame.grid(column = 0 , row = 1 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    daysListLabel.pack(fill = 'both' , side = 'left')
    backButton.grid(column = 0 , row = 2)
    confirmButton.grid(column = 1 , row = 2)

    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    confirmButton.label.bind('<1>' , lambda x: timeCardWin(emp ,days[daysListLabel.curselection()[0]].year , days[daysListLabel.curselection()[0]].month , days[daysListLabel.curselection()[0]].day))



def doneWin(text):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = Tk.Label(t , text = text +' Completed Sucsessfully' , width = 80 , height = 10)
    backButton = Tk.Button(t , text = 'OK' , command = lambda : t.destroy(), width = 80)

    #place widgets in window
    titleLabel.grid()
    backButton.grid()


def alertWin(text):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = Tk.Label(t , text = text , width = 80 , height = 10)
    backButton = Tk.Button(t , text = 'OK' , command = lambda : t.destroy(), width = 80)

    #place widgets in window
    titleLabel.grid()
    backButton.grid()


##################################
######## Root Window design #####
#################################
# create widgets
bName = MyLabel(root , height = setHeight(15), width = setWidth(100))
tLabel = TimeLabel(root , height = setHeight(50) , width = setWidth(50))
mainLog = Tk.Frame(root , height = setHeight(100) , width = setWidth(50))
scanLabel = ScanLabel(root , height = setHeight(50) , width = setWidth(50))

#configure Widgets
bName.label.configure(text = 'Firehouse Pizza' , font = 'verdana 35 bold')
scanLabel.label.config(text = 'Please Scan Card' , bg = 'red')
scanLabel.function = clockInWin
scanLabel.adminfunc = adminWin
scanLabel.tick()
tLabel.label.configure(font = 'verdana 30 bold')

# place Widgets
bName.grid(column = 0 , row = 0 , columnspan = 2)
tLabel.grid(column = 1 , row = 1)
mainLog.grid(column = 0 , row = 1, rowspan = 2)
scanLabel.grid(column = 1 , row = 2)

# bind widgets


# start program
root.mainloop()
