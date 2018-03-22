import sqlite3
import datetime


#create/connect to employee database
db = sqlite3.connect('TimeClock.sqlite')
# function to interface with sql database
dbi = db.execute


#make sure there is an emoloyee table
temp = dbi('SELECT name FROM sqlite_master WHERE type="table" AND name="employees"')
try:
    temp.fetchall()[0][0]

#if not create one
except:
    dbi('CREATE TABLE employees (id integer NOT NULL PRIMARY KEY ,name varchar NOT NULL,'
        'totalHours smallint NOT NULL DEFAULT 0,overtime smallint NOT NULL DEFAULT 0,hours smallint NOT NULL DEFAULT 0,'
        'onTen boolean NOT NULL DEFAULT 0,onLunch boolean NOT NULL DEFAULT 0,clockedIn boolean NOT NULL DEFAULT 0,'
        'lastTime varchar NOT NULL DEFAULT 0,uid varchar NOT NULL DEFAULT 0);')

#make sure there is a log table
temp = dbi('SELECT name FROM sqlite_master WHERE type="table" AND name="log"')
try:
    temp.fetchall()[0][0]

#if not create one and start pay period
except:
    dbi('CREATE TABLE log (id integer NOT NULL PRIMARY KEY , year smallint NOT NULL , '
        'month smallint NOT NULL ,day smallint NOT NULL , hour smallint NOT NULL , '
        'minute smallint NOT NULL ,second smallint NOT NULL , hours smallint NOT NULL , '
        'action smallint NOT NULL , uid varchar NOT NULL DEFAULT 0);')
    dtime = datetime.datetime.now()
    dbi('INSERT INTO log (year , month , day , hour , minute , second , hours , action , uid , id) values ('
        + str(dtime.year) + ' , ' + str(dtime.month)  + ' , ' + str(dtime.day) + ' , ' + str(dtime.hour) + ' , ' + str(dtime.minute) + ' , ' + str(
        dtime.second) + ' , 0 , 0 , "0" , 0);')
    db.commit()


#handles log table in database
class Log:
    def __init__(self, id):
        entry = dbi('SELECT * FROM log WHERE id =' + str(id) + ';').fetchall()[0]
        self. id = entry[0]
        self.year = entry[1]
        self.month = entry[2]
        self.day = entry[3]
        self.hour = entry[4]
        self.minute = entry[5]
        self.second = entry[6]
        self.hours = entry[7]
        self.action = entry[8]
        self.uid = entry[9]

    def update(self):
        dbi('UPDATE log SET month = ' + str(self.month) + ' , day = ' + str(self.day) + ' , hour = ' + str(self.hour) +
            ' , minute = ' + str(self.minute) + ' , second = ' + str(self.second) + ' , hours = ' + str(self.hours) +
            ' , action = ' + str(self.action) + ' , uid = "' + self.uid + '" WHERE id = ' +  str(self. id) + ';')
        db.commit()

    @classmethod
    def getEmployee(cls, uid):
        try:
            return dbi('SELECT * FROM log WHERE uid = "' + uid + '";')

        except:
            print('error in getEmployee function, mabey empty table')


    @classmethod
    def getDay(cls ,year , month , day , uid):
        try:
            return dbi('SELECT * FROM log WHERE uid = "' + str(uid) + '" AND day = ' + str(day) + ' AND month = ' + str(month) + ' AND year = ' + str(year) + ';')

        except:
            print('error in getDay function, mabey empty table')


    @classmethod
    def addEntry(cls , action , hours , uid , dtime):
        dbi('INSERT INTO log (year , month , day , hour , minute , second , hours , action , uid) values (' + str(dtime.year) + ' , ' + str(dtime.month) +
            ' , ' + str(dtime.day) + ' , ' + str(dtime.hour) + ' , ' + str(dtime.minute) + ' , ' + str(dtime.second) + ' , ' + str(hours) +
            ' , ' + str(action) + ' , "' + str(uid) + '");')
        db.commit()

    @classmethod
    def resetPeriod(cls):
        now = datetime.datetime.now()
        dbi('UPDATE log SET year = ' + str(now.year) + ' , month = ' + str(now.month) + ' , day = ' + str(now.day) + ' , hour = ' + str(now.hour) +
            ' , minute = ' + str(now.minute) + ' , second = ' + str(now.second) + '  WHERE id = 0 ;')
        db.commit()


#hadles employee database
class employee:
    def __init__(self, uid):
        self.uid = uid
        self.id = (dbi('SELECT id FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.name = (dbi('SELECT name FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.totalHours = (dbi('SELECT totalHours FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.overtime = (dbi('SELECT overtime FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.hours = (dbi('SELECT hours FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.onTen = (dbi('SELECT onTen FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.onLunch = (dbi('SELECT onLunch FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.clockedIn = (dbi('SELECT clockedIn FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0]
        self.format = '%Y-%m-%d %H:%M:%S'
        self.over = datetime.timedelta(0,0,0,0,0,8)
        self.overweek = datetime.timedelta(0,0,0,0,0,40)
        self.lastTime = datetime.datetime.strptime((dbi('SELECT lastTime FROM employees WHERE uid = ' + self.uid + ';')).fetchall()[0][0], self.format)

    @classmethod
    def newEmployee(cls , name , uid):
        temp = datetime.datetime.now()
        dbi('INSERT INTO employees (name , lastTime , uid) values ("' + name + '" , "' + temp.strftime('%Y-%m-%d %H:%M:%S') + '" , "' + uid + '");')
        db.commit()

    @classmethod
    def listEmployees(cls):
        return dbi('SELECT uid FROM employees;')


    def updateDB(self):
        dbi('UPDATE employees SET name = "' + self.name + '" ,  totalHours = ' + str(self.totalHours) +
            ' , overtime = ' + str(self.overtime) + ' , hours = ' + str(self.hours) + ' , onTen  = ' + str(self.onTen) +
            ', onLunch = ' + str(self.onLunch) + ', clockedIn = ' + str(self.clockedIn) + ' , lastTime = "' +
             self.lastTime.strftime(self.format) + '" , uid = "' + self.uid + '" WHERE id = ' + str(self.id) + ';')
        db.commit()


    def clockIn(self):
        if not self.clockedIn:
            if datetime.datetime.now().day != self.lastTime.day:
                self.hours = 0
            self.lastTime = datetime.datetime.now()
            Log.addEntry(1 , 0 , self.uid , self.lastTime)
            self.onTen = 0
            self.onLunch = 0
            self.clockedIn = 1
            self.updateDB()


    def startTen(self):
        if (not self.onTen) and self.clockedIn and (not self.onLunch):
            temp = (datetime.datetime.now() - self.lastTime).seconds
            self.hours += temp
            self.totalHours += temp
            self.onTen = 1
            self.lastTime = datetime.datetime.now()
            Log.addEntry(2 , temp , self.uid , self.lastTime)
            self.updateDB()


    def endTen(self):
        if self.onTen:
            temp = datetime.timedelta(0,600)
            temp2 = datetime.datetime.now() - self.lastTime
            self.lastTime = datetime.datetime.now()
            if temp2 <= temp:
                self.hours += temp2.seconds
                self.totalHours += temp2.seconds
                Log.addEntry(3 , temp2.seconds , self.uid , self.lastTime)
            else:
                self.hours += temp.seconds
                self.totalHours += temp.seconds
                Log.addEntry(3 , temp.seconds , self.uid , self.lastTime)
            self.onTen = 0
            self.updateDB()


    def startLunch(self):
        if (not self.onTen) and self.clockedIn  and (not self.onLunch):
            temp = (datetime.datetime.now() - self.lastTime).seconds
            self.hours += temp
            self.totalHours += temp
            self.onLunch = 1
            self.lastTime = datetime.datetime.now()
            Log.addEntry(4 , temp , self.uid , self.lastTime)
            self.updateDB()


    def endLunch(self):
        if self.onLunch:
            self.lastTime = datetime.datetime.now()
            Log.addEntry(5 , 0 , self.uid , self.lastTime)
            self.onLunch = 0
            self.updateDB()


    def clockOut(self):
        if self.clockedIn and (not self.onLunch) and (not self.onTen):
            temp = datetime.datetime.now() - self.lastTime
            self.hours += temp.seconds
            self.totalHours += temp.seconds
            self.lastTime = datetime.datetime.now()
            Log.addEntry(6 , temp.seconds , self.uid , self.lastTime)
            if self.hours > self.over.seconds:
                self.overtime += self.hours - self.over.seconds
            if self.totalHours > (self.overweek.seconds + self.overtime):
                self.overtime += self.totalHours - (self.overweek.seconds + self.overtime)
            self.clockedIn = 0
            self.updateDB()


    def destroy(self):
        dbi('DELETE FROM employees WHERE uid = "' + self.uid + '";')
        dbi('DELETE FROM log WHERE uid = "' + self.uid + '";')
        db.commit()


    def addTime(self, seconds , year , month , day):
        periodStart = Log(0)
        stime = datetime.datetime(periodStart.year, periodStart.month, periodStart.day)
        dtime = datetime.datetime(year , month , day)
        if dtime >= stime:
            print(seconds)
            self.totalHours += seconds
            self.updateDB()
        Log.addEntry(7 , seconds , self.uid , dtime)


    def subTime(self , seconds , year , month , day):
        periodStart = Log(0)
        stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
        dtime = datetime.datetime(year , month , day)
        if dtime >= stime :
            self.totalHours -= seconds
            self.updateDB()
        Log.addEntry(8 , seconds , self.uid , self.lastTime)


    def addOvertime(self, seconds , year , month , day):
        periodStart = Log(0)
        stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
        dtime = datetime.datetime(year , month , day)
        if dtime >= stime :
            self.totalHours += seconds
            self.overtime += seconds
            self.updateDB()
        Log.addEntry(9 , seconds , self.uid , self.lastTime)


    def subOvertime(self, seconds , year , month , day):
        periodStart = Log(0)
        stime = datetime.datetime(periodStart.year , periodStart.month , periodStart.day)
        dtime = datetime.datetime(year , month , day)
        if dtime >= stime :
            self.overtime -= seconds
            self.updateDB()
        Log.addEntry(10 , seconds , self.uid , self.lastTime)
