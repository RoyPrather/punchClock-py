!/usr/bin/python
from Gui import *
import RPi.GPIO as GPIO
# create main window
root = Tk.Tk()
root.attributes('-fullscreen' , True)
root.lift()
root.focus_force()

#crate sizing variables   (oversized in some places to fix test screen)
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()


def setWidth(percent):
    return((screenWidth / 100) * percent)


def setHeight(percent):
    return((screenHeight / 100) * percent)


# Bring up Clock in Screen
#TODO: view timecard button
def clockInWin(uid) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create employee class instance
    emp = employee(uid)

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
    buttonBox = Tk.Frame(t , width = setWidth(100) , height = setHeight(12))
    sendMessageButton = MyButton(buttonBox , width = setWidth(25) , height = setHeight(12))
    timeCardButton = MyButton(buttonBox , width = setWidth(25) , height = setHeight(12))
    backButton = MyButton(buttonBox , width = setWidth(25) , height = setHeight(12))

    # configure widgets
    nameLabel.label.config(text = emp.name)
    hoursTitle.label.config(text = 'Total Hours This Period')
    hoursTotal.label.config(text = str(round((emp.totalHours - emp.overtime) / 3600.0 , 2)))
    hoursTotal.emp = emp
    hoursTotal.tick()
    todayTitle.label.config(text = 'Hours Worked Today')
    todayHours.label.config(text = round(emp.hours / 3600.0 , 2))
    todayHours.emp = emp
    todayHours.tick()
    overTitle.label.config(text = 'Over Time')
    overHours.label.config(text = round(emp.overtime / 3600.0 , 2))

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
    lunchInButton.alertFunction = earlyLunchWin
    lunchInButton.tick()
    sendMessageButton.label.configure(text = 'Send Message')
    backButton.label.configure(text = 'Done')
    timeCardButton.label.configure(text = 'Timecard')

    # place widgets in window
    nameLabel.grid(column = 0 , row = 0 , columnspan = 2)
    hoursTitle.grid(column = 0 , row = 1)
    hoursTotal.grid(column = 0 , row = 2)
    todayTitle.grid(column = 0 , row = 3)
    todayHours.grid(column = 0 , row = 4)
    overTitle.grid(column = 0 , row = 5)
    overHours.grid(column = 0 , row = 6)
    placeHolder1.grid(column = 0 , row = 7)


    clockInButton.grid(column = 1 , row = 1)
    tenMinOutButton.grid(column = 1 , row = 2)
    tenMinInButton.grid(column = 1 , row = 3)
    lunchOutButton.grid(column = 1 , row = 4)
    lunchInButton.grid(column = 1 , row = 5)
    clockOutButton.grid(column = 1 , row = 6)
    placeHolder2.grid(column = 1 , row = 7)

    buttonBox.grid(row = 8 , column = 0 , columnspan = 2)
    backButton.grid(column = 0 , row = 0)
    sendMessageButton.grid(column = 1 , row = 0)
    timeCardButton.grid(column = 2 , row = 0)

    # bind widgets
    sendMessageButton.label.bind('<1>' , lambda x: sendMessageWin(emp.name))
    backButton.label.bind('<1>' , lambda x: t.destroy())
    timeCardButton.label.bind('<1>' , lambda x: (employeeTimeCardDayWin(emp), t.destroy()))


def employeeTimeCardDayWin(emp):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    confirmButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    ListboxFrame = Tk.Frame(t, width = setWidth(80) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    daysListLabel = Tk.Listbox(ListboxFrame , width = 30 , yscrollcommand = scrollBar.scrollBar.set , selectmode = 'single' , font = font)

    #configure widgets
    titleLabel.label.configure(text = 'Choose Day To Veiw')
    backButton.label.configure(text = 'Cancel')
    confirmButton.label.configure(text = 'OK')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = daysListLabel.yview)

    periodStart = Log(0)
    stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
    dtime = datetime.datetime.now()
    print(dtime)
    print(stime)
    tdelta = (dtime - stime).days + 1
    print(tdelta)
    days = []
    count = 0
    for day in range(tdelta):
        temp = dtime - datetime.timedelta(day)
        daysListLabel.insert(count, str(temp.month) +'/'+ str(temp.day) +'/'+ str(temp.year))
        days.insert(count, temp)
        count += 1

    #place widgets
    titleLabel.grid(column = 0 , row = 0 , columnspan = 2)
    ListboxFrame.grid(column = 0 , row = 1 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    daysListLabel.pack(fill = 'both' , side = 'left')
    backButton.grid(column = 0 , row = 2)
    confirmButton.grid(column = 1 , row = 2)

    #bind widgets
    backButton.label.bind('<1>' , lambda x: (clockInWin(emp.uid) , t.destroy()))
    confirmButton.label.bind('<1>' , lambda x: (employeeTimeCardWin(emp ,days[daysListLabel.curselection()[0]].year , days[daysListLabel.curselection()[0]].month , days[daysListLabel.curselection()[0]].day) , t.destroy()))


def employeeTimeCardWin(emp , year , month , day) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    ListboxFrame = Tk.Frame(t, width = setWidth(100) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    LogListbox = Tk.Listbox(ListboxFrame , width = setWidth(90) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)
    hoursLabel = MyLabel(t , width = setWidth(100) , height = setHeight(10))

    #configure widgets
    titleLabel.label.configure(text = emp.name)
    backButton.label.configure(text = 'Back')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = LogListbox.yview)

    #place widgets
    titleLabel.grid(row = 0 , column = 0 , columnspan = 2)
    ListboxFrame.grid(row = 1 , column = 0 , columnspan = 2)
    hoursLabel.grid(row = 2 , column = 0 , columnspan = 2)
    backButton.grid(row = 3 , column = 0)
    scrollBar.pack(fill = 'y' , side = 'right')
    LogListbox.pack(fill = 'both' , side = 'left')

    hours = 0
    for entry in Log.getDay(year , month , day, emp.uid):
        if entry[8] == 1:
            LogListbox.insert('end' , 'Clocked In At:                        ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 2 :
            LogListbox.insert('end' , 'Started A Ten At:                  ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 3 :
            LogListbox.insert('end' , 'Returned From Ten At:         ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 4 :
            LogListbox.insert('end' , 'Started A Lunch At:              ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 5 :
            LogListbox.insert('end' , 'Returned From Lunch At:     ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 6 :
            LogListbox.insert('end' , 'Clocked Out At:                     ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 7 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 8 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours -= entry[7]

        elif entry[8] == 9 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 3600.0 , 2)) + 'Overtime Hours')
            hours += entry[7]

        elif entry[8] == 10 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 3600.0 , 2)) + 'Overtime Hours')
            hours -= entry[7]

    hoursLabel.label.configure(text ='Hours This Day  ' + str(round(hours / 3600.0 , 2)))

   #bind widgets
    backButton.label.bind('<1>' , lambda x: (employeeTimeCardDayWin(emp) , t.destroy()))

#TODO: add admin override
def earlyLunchWin(emp):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(20))
    backButton = MyButton(t , width = setWidth(100) , height = setHeight(20))
    overrideButton = LunchOverrideButton(t , width = setWidth(100) , height = setHeight(20))

    #configure widgets
    titleLabel.label.configure(text = 'Sorry, You Must Be On Lunch For 30 Min!')
    backButton.label.configure(text = 'OK')
    overrideButton.mLabel = titleLabel
    overrideButton.emp = emp
    overrideButton.tick()

    #place widgets in window
    titleLabel.grid()
    backButton.grid()
    overrideButton.grid()
    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())

# Bring up  admin screen
def adminWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()
    # create widgets
    viewMessageButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    viewLogButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    newEmployeeButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    createReportButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    newAdminButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    employeeCheckInButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    replaceCardButton = MyButton(t, width = setWidth(50) , height = setHeight(25))
    closeButton = MyButton(t , height = setHeight(15) , width = setWidth(25))
    backButton = MyButton(t , height = setHeight(15) , width = setWidth(25))

    #configure Widgets
    viewMessageButton.label.configure(text = 'View Messages')
    viewLogButton.label.configure(text = 'View Employee Hours')
    newEmployeeButton.label.configure(text = 'Create New Employee')
    createReportButton.label.configure(text = 'End Pay Period')
    newAdminButton.label.configure(text = 'Create New Admin Card')
    employeeCheckInButton.label.configure(text = 'View Employee Screen')
    replaceCardButton.label.configure(text = 'Replace Lost Card')
    backButton.label.configure(text ='Back')
    closeButton.label.configure(text = 'Close Program')

    # place widgets in window
    viewMessageButton.grid(row = 0 , column = 0)
    newEmployeeButton.grid(row = 0 , column = 1)
    createReportButton.grid(row = 1 , column = 0)
    viewLogButton.grid(row = 1 , column  = 1)
    newAdminButton.grid(row = 2 , column = 0)
    employeeCheckInButton.grid(row = 2 , column = 1)
    replaceCardButton.grid(row = 3 , column = 0)
    backButton.grid(row = 4 , column = 0)
    closeButton.grid(row = 4 , column = 1)

    # bind widgets
    viewMessageButton.label.bind('<1>' , lambda x: readMessageWin())
    viewLogButton.label.bind('<1>' , lambda x: timeCardListWin())
    newEmployeeButton.label.bind('<1>' , lambda x: newEmployeeWin())
    createReportButton.label.bind('<1>' , lambda x: reportWin())
    newAdminButton.label.bind('<1>' , lambda x: programCardWin('admin'))
    employeeCheckInButton.label.bind('<1>' , lambda x: employeeCheckInListWin())
    replaceCardButton.label.bind('<1>' , lambda x: replaceCardListWin())
    backButton.label.bind('<1>' , lambda x: t.destroy())
    closeButton.label.bind('<1>' , lambda x : closeProgramWin())

#employee list for time cards
def timeCardListWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    submitButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    nameFrame = Tk.Listbox(ListboxFrame , width = setWidth(75) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)

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
            nameFrame.insert(count , emp.name + '  :  ' + str(round((emp.totalHours - emp.overtime) / 3600.0 , 2))  +
                             '  Hours / ' + str(round(emp.overtime / 3600.0 , 2)) + '  Overtime')
            count += 1

    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    submitButton.label.bind('<1>' , lambda x: (timeCardDayWin(emps[nameFrame.curselection()[0]]) , t.destroy()))


def timeCardDayWin(emp):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    confirmButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    ListboxFrame = Tk.Frame(t, width = setWidth(80) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    daysListLabel = Tk.Listbox(ListboxFrame , width = 30 , yscrollcommand = scrollBar.scrollBar.set , selectmode = 'single' , font = font)

    #configure widgets
    titleLabel.label.configure(text = 'Choose Day To Veiw')
    backButton.label.configure(text = 'Cancel')
    confirmButton.label.configure(text = 'OK')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = daysListLabel.yview)

    periodStart = Log(0)
    stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
    dtime = datetime.datetime.now()
    print(dtime)
    print(stime)
    tdelta = (dtime - stime).days + 1
    print(tdelta)
    days = []
    count = 0
    for day in range(tdelta):
        temp = dtime - datetime.timedelta(day)
        daysListLabel.insert(count, str(temp.month) +'/'+ str(temp.day) +'/'+ str(temp.year))
        days.insert(count, temp)
        count += 1

    #place widgets
    titleLabel.grid(column = 0 , row = 0 , columnspan = 2)
    ListboxFrame.grid(column = 0 , row = 1 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    daysListLabel.pack(fill = 'both' , side = 'left')
    backButton.grid(column = 0 , row = 2)
    confirmButton.grid(column = 1 , row = 2)

    #bind widgets
    backButton.label.bind('<1>' , lambda x: (timeCardListWin() , t.destroy()))
    confirmButton.label.bind('<1>' , lambda x: (timeCardWin(emp ,days[daysListLabel.curselection()[0]].year , days[daysListLabel.curselection()[0]].month , days[daysListLabel.curselection()[0]].day) , t.destroy()))


def timeCardWin(emp , year , month , day) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    editButton = MyButton(t, width = setWidth(25) , height = setHeight(25))
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
    for entry in Log.getDay(year , month , day, emp.uid):
        if entry[8] == 1:
            LogListbox.insert('end' , 'Clocked In At:                        ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 2 :
            LogListbox.insert('end' , 'Started A Ten At:                  ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 3 :
            LogListbox.insert('end' , 'Returned From Ten At:         ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 4 :
            LogListbox.insert('end' , 'Started A Lunch At:              ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 5 :
            LogListbox.insert('end' , 'Returned From Lunch At:     ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 6 :
            LogListbox.insert('end' , 'Clocked Out At:                     ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 7 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 8 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours -= entry[7]

        elif entry[8] == 9 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 3600.0 , 2)) + 'Overtime Hours')
            hours += entry[7]

        elif entry[8] == 10 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 3600.0 , 2)) + 'Overtime Hours')
            hours -= entry[7]

    hoursLabel.label.configure(text ='Hours This Day  ' + str(round(hours / 3600.0 , 2)))

   #bind widgets
    backButton.label.bind('<1>' , lambda x: (timeCardDayWin(emp) , t.destroy()))
    editButton.label.bind('<1>' , lambda x: (editTimeCardWin(emp , year , month , day) , t.destroy()))


def editTimeCardWin(emp , year , month , day):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    hoursTitleLabel = MyLabel(t , width = setWidth(50) , height = setHeight(15))
    overTitleLabel = MyLabel(t , width = setWidth(50) , height = setHeight(15))
    hoursLabel = TotalHoursLabel(t , width = setWidth(50) , height = setHeight(15))
    overLabel = OverHoursLabel(t , width = setWidth(50) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(30) , height = setHeight(15))
    addOverButton = MyButton(t , width = setWidth(45) , height = setHeight(15))
    subOverButton = MyButton(t , width = setWidth(45) , height = setHeight(15))
    addMinuteButton = MyButton(t , width = setWidth(30) , height = setHeight(15))
    subMinuteButton = MyButton(t , width = setWidth(30) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(40))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(60))
    numSelectBox = Tk.Listbox(ListboxFrame , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)


    #configure widgets
    hoursTitleLabel.label.configure(text = 'Add or Remove Regular Time')
    overTitleLabel.label.configure(text = 'Add or Remove Overtime')
    hoursLabel.emp = emp
    hoursLabel.tick()
    overLabel.emp = emp
    overLabel.tick()
    addOverButton.label.configure(text = 'Add Overtime Minutes')
    subOverButton.label.configure(text = 'Remove Overtime Minutes')
    addMinuteButton.label.configure(text = 'Add Minutes')
    subMinuteButton.label.configure(text = 'Remove Minutes')
    backButton.label.configure(text = 'Back')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = numSelectBox.yview)
    for i in range(60):
        numSelectBox.insert(i, 60 - i)

    #place widgets in window
    hoursTitleLabel.grid(row = 0 , column = 0 )
    overTitleLabel.grid(row = 0 , column = 1 )
    hoursLabel.grid(row = 1 , column = 0 )
    overLabel.grid(row = 1 , column = 1)
    ListboxFrame.grid(row = 2 , column = 0 , columnspan = 2)
    addMinuteButton.grid(row = 3 , column = 0)
    subMinuteButton.grid(row = 3 , column = 1)
    addOverButton.grid(row = 4 , column = 0)
    subOverButton.grid(row = 4 , column = 1)
    backButton.grid(row = 5 , column = 0 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    numSelectBox.pack(fill = 'both' , side = 'left')

    #bind widgets
    backButton.label.bind('<1>' , lambda x: (timeCardWin(emp , year , month , day) , t.destroy()))
    addMinuteButton.label.bind('<1>' , lambda x: emp.addTime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))
    subMinuteButton.label.bind('<1>' , lambda x: emp.subTime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))
    addOverButton.label.bind('<1>' , lambda x: emp.addOvertime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))
    subOverButton.label.bind('<1>' , lambda x: emp.subOvertime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))


def endPeriod():
    now = datetime.datetime.now()
    totalHours = 0
    totalOver = 0
    filename = 'EmployeeHours-' + str(now.month) + '-' + str(now.day) + '-' + str(now.year) + '.txt'
    file = open(filename , 'w+')
    temp = 'Hours Summary'
    file.write('{0:^60}'.format(temp))
    file.write('\n')
    for uid in employee.listEmployees():
        emp = employee(uid[0])
        if emp.name != 'admin':
            if emp.onTen:
                emp.endTen()
            if emp.onLunch:
                emp.endLunch()
            if emp.clockedIn:
                emp.clockOut()
            temp = ['Employee Name' , 'Regular Hours' , 'Overtime Hours']
            file.write('{0[0]:<30}{0[1]:^15}{0[2]>15}'.format(temp))
            file.write('{0:<30}{1:^15}{2:>15}\n'.format(emp.name , round((emp.totalHours - emp.overtime) / 3600.0 , 2)  , str(round(emp.overtime / 3600.00 , 2))))
            totalHours += emp.totalHours - emp.overtime
            totalOver += emp.overtime
            emp.overtime = 0
            emp.totalHours = 0
            emp.hours = 0
            emp.updateDB()
    file.write('\n Total Regular Hours Paid:   \t' + str(round(totalHours / 3600.00 , 2)) + '\n')
    file.write(' Total Overtime Paid:    \t' + str(round(totalOver / 3600.00 , 2)) + '\n')
    file.close()


def reportWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(30) , height = setHeight(15))
    hoursLabel = MyLabel(t , width = setWidth(30) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    editButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    endPeriodButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    nameFrame = Tk.Listbox(ListboxFrame , width = setWidth(75) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)

    #configure widgets
    titleLabel.label.configure(text = 'Total Hours:')
    editButton.label.configure(text = 'Edit Employee')
    endPeriodButton.label.configure(text = 'End Pay Period')
    backButton.label.configure(text = 'Back')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = nameFrame.yview)

    #place widgets in window
    titleLabel.grid(row = 0 , column = 0)
    hoursLabel.grid(row = 0 , column = 1)
    ListboxFrame.grid(row = 1 , column = 0 , columnspan = 3)
    scrollBar.pack(fill = 'y' , side = 'right')
    nameFrame.pack(fill = 'both' , side = 'left')
    backButton.grid(row = 2 , column = 0)
    editButton.grid(row = 2 , column  = 1)
    endPeriodButton.grid(row = 2 , column = 2)


    #place list of employees into nameFrame
    count = 0
    emps = []
    totalHours = 0
    for uid in employee.listEmployees():
        emp = employee(uid[0])
        if emp.name != 'admin':
            emps.insert(count , emp)
            nameFrame.insert(count , emp.name + '    :     ' + str(round(emp.totalHours / 3600.0 , 2))  + '  Hours')
            totalHours += emp.totalHours
            count += 1

    hoursLabel.label.configure(text = round(totalHours / 3600.0 , 2))
    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    editButton.label.bind('<1>' , lambda x: (reportTimeCardDayWin(emps[nameFrame.curselection()[0]]), t.destroy()))
    endPeriodButton.label.bind('<1>' , lambda x:(Log.resetPeriod(), endPeriod() , t.destroy()))


def reportTimeCardDayWin(emp):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    confirmButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    ListboxFrame = Tk.Frame(t, width = setWidth(80) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    daysListLabel = Tk.Listbox(ListboxFrame , width = 30 , yscrollcommand = scrollBar.scrollBar.set , selectmode = 'single' , font = font)

    #configure widgets
    titleLabel.label.configure(text = 'Choose Day To Veiw')
    backButton.label.configure(text = 'Cancel')
    confirmButton.label.configure(text = 'OK')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = daysListLabel.yview)

    periodStart = Log(0)
    stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
    dtime = datetime.datetime.now()
    print(dtime)
    print(stime)
    tdelta = (dtime - stime).days + 1
    print(tdelta)
    days = []
    count = 0
    for day in range(tdelta):
        temp = dtime - datetime.timedelta(day)
        daysListLabel.insert(count, str(temp.month) +'/'+ str(temp.day) +'/'+ str(temp.year))
        days.insert(count, temp)
        count += 1

    #place widgets
    titleLabel.grid(column = 0 , row = 0 , columnspan = 2)
    ListboxFrame.grid(column = 0 , row = 1 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    daysListLabel.pack(fill = 'both' , side = 'left')
    backButton.grid(column = 0 , row = 2)
    confirmButton.grid(column = 1 , row = 2)

    #bind widgets
    backButton.label.bind('<1>' , lambda x: (reportWin() , t.destroy()))
    confirmButton.label.bind('<1>' , lambda x: (reportTimeCardWin(emp ,days[daysListLabel.curselection()[0]].year , days[daysListLabel.curselection()[0]].month , days[daysListLabel.curselection()[0]].day) , t.destroy()))


def reportTimeCardWin(emp , year , month , day) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    #create widgets
    titleLabel = MyLabel(t, width = setWidth(100) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(25))
    editButton = MyButton(t, width = setWidth(25) , height = setHeight(25))
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
    for entry in Log.getDay(year , month , day, emp.uid):
        if entry[8] == 1:
            LogListbox.insert('end' , 'Clocked In At:                        ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 2 :
            LogListbox.insert('end' , 'Started A Ten At:                  ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 3 :
            LogListbox.insert('end' , 'Returned From Ten At:         ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 4 :
            LogListbox.insert('end' , 'Started A Lunch At:              ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 5 :
            LogListbox.insert('end' , 'Returned From Lunch At:     ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 6 :
            LogListbox.insert('end' , 'Clocked Out At:                     ' + str(entry[4]).zfill(2) + ':' + str(entry[5]).zfill(2) + ':' + str(
                entry[6]).zfill(2) + '.        Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 7 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours += entry[7]

        elif entry[8] == 8 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 3600.0 , 2)) + ' Hours')
            hours -= entry[7]

        elif entry[8] == 9 :
            LogListbox.insert('end' , 'Manual Change.                Added ' + str(round(entry[7] / 3600.0 , 2)) + 'Overtime Hours')
            hours += entry[7]

        elif entry[8] == 10 :
            LogListbox.insert('end' , 'Manual Change.                Removed ' + str(round(entry[7] / 3600.0 , 2)) + 'Overtime Hours')
            hours -= entry[7]

    hoursLabel.label.configure(text ='Hours This Day  ' + str(round(hours / 3600.0 , 2)))

   #bind widgets
    backButton.label.bind('<1>' , lambda x: (reportTimeCardDayWin(emp) , t.destroy()))
    editButton.label.bind('<1>' , lambda x: (reportEditTimeCardWin(emp , year , month , day) , t.destroy()))


def reportEditTimeCardWin(emp , year , month , day):
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    hoursTitleLabel = MyLabel(t , width = setWidth(50) , height = setHeight(15))
    overTitleLabel = MyLabel(t , width = setWidth(50) , height = setHeight(15))
    hoursLabel = TotalHoursLabel(t , width = setWidth(50) , height = setHeight(15))
    overLabel = OverHoursLabel(t , width = setWidth(50) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(30) , height = setHeight(15))
    addOverButton = MyButton(t , width = setWidth(45) , height = setHeight(15))
    subOverButton = MyButton(t , width = setWidth(45) , height = setHeight(15))
    addMinuteButton = MyButton(t , width = setWidth(30) , height = setHeight(15))
    subMinuteButton = MyButton(t , width = setWidth(30) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(40))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(60))
    numSelectBox = Tk.Listbox(ListboxFrame , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)


    #configure widgets
    hoursTitleLabel.label.configure(text = 'Add or Remove Regular Time')
    overTitleLabel.label.configure(text = 'Add or Remove Overtime')
    hoursLabel.emp = emp
    hoursLabel.tick()
    overLabel.emp = emp
    overLabel.tick()
    addOverButton.label.configure(text = 'Add Overtime Minutes')
    subOverButton.label.configure(text = 'Remove Overtime Minutes')
    addMinuteButton.label.configure(text = 'Add Minutes')
    subMinuteButton.label.configure(text = 'Remove Minutes')
    backButton.label.configure(text = 'Back')
    ListboxFrame.pack_propagate(0)
    scrollBar.scrollBar.config(command = numSelectBox.yview)
    for i in range(60):
        numSelectBox.insert(i, 60 - i)

    #place widgets in window
    hoursTitleLabel.grid(row = 0 , column = 0 )
    overTitleLabel.grid(row = 0 , column = 1 )
    hoursLabel.grid(row = 1 , column = 0 )
    overLabel.grid(row = 1 , column = 1)
    ListboxFrame.grid(row = 2 , column = 0 , columnspan = 2)
    addMinuteButton.grid(row = 3 , column = 0)
    subMinuteButton.grid(row = 3 , column = 1)
    addOverButton.grid(row = 4 , column = 0)
    subOverButton.grid(row = 4 , column = 1)
    backButton.grid(row = 5 , column = 0 , columnspan = 2)
    scrollBar.pack(fill = 'y' , side = 'right')
    numSelectBox.pack(fill = 'both' , side = 'left')

    #bind widgets
    backButton.label.bind('<1>' , lambda x: (reportTimeCardWin(emp , year , month , day) , t.destroy()))
    addMinuteButton.label.bind('<1>' , lambda x: emp.addTime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))
    subMinuteButton.label.bind('<1>' , lambda x: emp.subTime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))
    addOverButton.label.bind('<1>' , lambda x: emp.addOvertime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))
    subOverButton.label.bind('<1>' , lambda x: emp.subOvertime(datetime.timedelta(0 ,0 ,0,0,60 - numSelectBox.curselection()[0]).seconds , year , month , day))


def newEmployeeWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(25))
    nameEntry = Tk.Entry(t , width = 30 )
    submitButton = MyButton(t , width = setWidth(50) , height = setHeight(25))
    backButton = MyButton(t , width = setWidth(50) , height = setHeight(25))

    #configure widgets
    submitButton.label.configure( text = 'Create Employee')
    nameEntry.configure(font = largeFont)
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


def programCardWin(name) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    dLabel = MyLabel(t , width = setWidth(100) , height = setHeight(75))
    kButton = ProgramingButton(t , width = setWidth(50) , height = setHeight(25))
    backButton = MyButton(t , width = setWidth(50) , height = setHeight(25))

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


# Bring up Messge sending window
#TODO: create a table for messages/ create a hadleing class /fix ui
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
#TODO: fix ui
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


def closeProgramWin():
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLable = MyLabel(t , width = setWidth(100) , height = setHeight(30))
    closeButton = MyButton(t  , width = setWidth(30) , height = setHeight(20))
    backButton = MyButton(t , width = setWidth(30) , height = setHeight(20))

    #configure widgets
    titleLable.label.configure(text = 'Are You Sure' , font = largeFont)
    closeButton.label.configure(text = '!!!CLOSE PROGRAM!!!')
    backButton.label.configure(text = 'Cancel')

    #place widgets in window
    titleLable.grid(row = 0 , column = 0 , columnspan = 2)
    closeButton.grid(row = 1 , column = 1)
    backButton.grid(row = 1 , column = 0)

    #bind Widgets
    closeButton.label.bind('<1>' , lambda x: (GPIO.cleanup() , root.destroy()))
    backButton.label.bind('<1>' , lambda x: t.destroy())


def employeeCheckInListWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    submitButton = MyButton(t , width = setWidth(50) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    nameFrame = Tk.Listbox(ListboxFrame , width = setWidth(75) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)

    #configure widgets
    titleLabel.label.configure(text = 'Choose an Employee to Veiw')
    submitButton.label.configure(text = 'View Clock In Screen')
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
            nameFrame.insert(count , emp.name + '  :  ' + str(round((emp.totalHours - emp.overtime) / 3600.0 , 2))  +
                             '  Hours / ' + str(round(emp.overtime / 3600.0 , 2)) + '  Overtime')
            count += 1

    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    submitButton.label.bind('<1>' , lambda x: clockInWin(emps[nameFrame.curselection()[0]].uid))


def replaceCardListWin() :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    titleLabel = MyLabel(t , width = setWidth(100) , height = setHeight(15))
    backButton = MyButton(t , width = setWidth(25) , height = setHeight(15))
    submitButton = MyButton(t , width = setWidth(50) , height = setHeight(15))
    ListboxFrame = Tk.Frame(t, width = setWidth(85) , height = setHeight(70))
    scrollBar = MyScrollBar(ListboxFrame , width = setWidth(10) , height = setHeight(70))
    nameFrame = Tk.Listbox(ListboxFrame , width = setWidth(75) , height = setHeight(70) , yscrollcommand = scrollBar.scrollBar.set , selectmode ='single' , font = font)

    #configure widgets
    titleLabel.label.configure(text = 'Choose an Employee to Veiw')
    submitButton.label.configure(text = 'Create New Card')
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
            nameFrame.insert(count , emp.name + '  :  ' + str(round((emp.totalHours - emp.overtime) / 3600.0 , 2))  +
                             '  Hours / ' + str(round(emp.overtime / 3600.0 , 2)) + '  Overtime')
            count += 1

    #bind widgets
    backButton.label.bind('<1>' , lambda x: t.destroy())
    submitButton.label.bind('<1>' , lambda x: (replaceCardWin(emps[nameFrame.curselection()[0]]), t.destroy()))


def replaceCardWin(emp) :
    # create window
    t = Tk.Toplevel(root)
    t.attributes('-fullscreen' , True)
    t.lift()

    # create widgets
    dLabel = MyLabel(t , width = setWidth(100) , height = setHeight(75))
    kButton = ReplaceCardButton(t , width = setWidth(50) , height = setHeight(25))
    backButton = MyButton(t , width = setWidth(50) , height = setHeight(25))

    # configure widgets
    dLabel.label.configure(text = 'Scan New Card')
    kButton.emp = emp
    kButton.mLabel = dLabel
    kButton.tick()
    backButton.label.configure(text = 'Cancel')

    # place widgets in window
    dLabel.grid(row = 0 , column = 0 , columnspan = 2)
    kButton.grid(row = 1 , column = 1)
    backButton.grid(row = 1 , column = 0)

    # bind widgets
    backButton.label.bind('<1>' , lambda x : t.destroy())





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
scanLabel.startUp()
tLabel.label.configure(font = 'verdana 30 bold')

# place Widgets
bName.grid(column = 0 , row = 0 , columnspan = 2)
tLabel.grid(column = 1 , row = 1)
mainLog.grid(column = 0 , row = 1, rowspan = 2)
scanLabel.grid(column = 1 , row = 2)

# start program
root.mainloop()