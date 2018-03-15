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
    viewLogButton.label.bind('<1>' , lambda x: showLog())
    newEmployeeButton.label.bind('<1>' , lambda x: newEmployeeWin())
    createReportButton.label.bind('<1>' , lambda x: reportWin())
    newAdminButton.label.bind('<1>' , lambda x: programingWin('admin'))
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
    submitButton.label.bind('<1>' , lambda x: (programingWin(nameEntry.get()), t.destroy()))
    backButton.label.bind('<1>' , lambda x: t.destroy())


# Bring up new admin screen
def programingWin(name) :
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
   # bind widgets


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


#Show log for editing .... by name?
def showLog() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(15))
    canvasBox = Tk.Frame(t, width = setWidth(85) , height = setHeight(70))
    backButton = BlueButton(t , width = setWidth(25) , height = setHeight(15))
    scrollBar = MyScrollBar(canvasBox , width = setWidth(10) , height = setHeight(70))
    nameFrame = Tk.Listbox(canvasBox , width = setWidth(75) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single')

    #configure widgets
    titleLabel.label.configure(text = 'Choose and Employee to Veiw')
    backButton.label.configure(text = 'Back')
    canvasBox.pack_propagate(0)
    scrollBar.scrollBar.config(command = nameFrame.yview)

    #place widgets in window
    titleLabel.grid(column = 0 , row = 0 , columnspan = 2)
    canvasBox.grid(column = 0 , row = 1 )
    scrollBar.pack(fill = 'y' , side = 'right')
    nameFrame.pack(fill = 'both' , side = 'left')
    backButton.grid(column = 0 , row = 2)

    #TODO: place list of employees into nameFrame
    for uid in employee.listEmployees():
        emp = employee(uid[0])
        if emp.name != 'admin':
            nameFrame.insert('end' , emp.name)

    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())

def timeCard(emp) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    labelFrame = Tk.Frame(t, width = setWidth(100) , height = setHeight(60))
    backButton = BlueButton(t , width = setWidth(25) , height = setHeight(25))

    #configure widgets
    titleLabel.label.configure(text = emp.name)
    backButton.label.configure(text = 'Back')
    now = datetime.datetime.now()

    #place widgets
    titleLabel.grid(row = 0 , column = 0 , columnspan = 2)
    labelFrame.grid(row = 1 , column = 0 , columnspan = 2)
    backButton.grid(row = 3 , column = 0)
    rownum = 0
    for entry in log.getDay(now.month , now.day, emp.id):
        label = MyLabel(labelFrame , width = setWidth(100) , height = setHeight(10))
        if entry[5] == 0:
            label.label.configure(text = 'In At: ' + str(entry[1]) + ':' + str(entry[2]) + ':' + str(entry[3]) + ':' + str(entry[4]))

        else:
            label.label.configure(text = 'Out At: ' + str(entry[1]) + ':' + str(entry[2]) + ':' + str(entry[3]) + ':' +
                                         str(entry[4]) +'.   Added ' + datetime.time.strftime(datetime.timedelta(0,entry[5])) + ' Hours')

        label.grid(row = rownum, column = 0)
        rownum += 1

   #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())


#confirmation win
def confirmWin(title , action) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = Tk.Label(t , text = 'Are You Sure You Want To ' + title +'?' , width = 80)
    confirmButton = Tk.Button(t , text = 'Yes!' , width = 80 , command = lambda : (action() , t.destroy()))
    backButton = Tk.Button(t , text = 'Cancel' , command = lambda : t.destroy(), width = 80)

    #place widgets in window
    titleLabel.grid()
    confirmButton.grid()
    backButton.grid()


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
