import sqlite3
import datetime


#create/connect to employee database
db = sqlite3.connect('TimeClock.sqlite')
# function to interface with sql database
dbi = db.execute

temp = dbi('SELECT name FROM sqlite_master WHERE type="table" AND name="employees"')
try:
    temp.fetchall()[0][0]

except:
    dbi('CREATE TABLE employees (id integer NOT NULL PRIMARY KEY ,name varchar NOT NULL,'
         'totalHours smallint NOT NULL DEFAULT 0,overtime smallint NOT NULL DEFAULT 0,hours smallint NOT NULL DEFAULT 0,'
         'onTen boolean NOT NULL DEFAULT 0,onLunch boolean NOT NULL DEFAULT 0,clockedIn boolean NOT NULL DEFAULT 0,'
         'lastTime varchar NOT NULL DEFAULT 0,uid varchar NOT NULL DEFAULT 0);')


temp = dbi('SELECT name FROM sqlite_master WHERE type="table" AND name="log"')
try:
    temp.fetchall()[0][0]

except:
    dbi('CREATE TABLE log (id integer NOT NULL PRIMARY KEY ,'
         'month smallint NOT NULL ,day smallint NOT NULL , hour smallint NOT NULL , '
         'minute smallint NOT NULL ,second smallint NOT NULL , hours smallint NOT NULL , '
         'action integer NOT NULL , uid varchar NOT NULL DEFAULT 0);')


#handles log table in database
class log:
    def __init__(self, id):
        entry = dbi('SELECT * FROM log WHERE id =' + str(id) + ';').fetchall()[0]
        self. id = entry[0]
        self.month = entry[1]
        self.day = entry[2]
        self.hour = entry[3]
        self.minute = entry[4]
        self.second = entry[5]
        self.hours = entry[6]
        self.action = entry[7]
        self.uid = entry[8]

    def update(self):
        dbi('UPDATE log SET month = ' + str(self.month) + ' , day = ' + str(self.day) + ' , hour = ' + str(self.hour) +
            ' , minute = ' + str(self.minute) + ' , second = ' + str(self.second) + ' , hours = ' + str(self.hours) +
            ' , action = ' + self.action + ' WHERE id = ' +  str(self. id) + ';')
        db.commit()

    def addTime(self, hour , minute , second):
        emp = employee(self.uid)
        emp.hours += abs(datetime.timedelta(0 , second , 0 , 0 , minute , hour , 0).seconds - datetime.timedelta(
            0 , self.second , 0 , 0 , self.minute , self.hour , 0).seconds)
        emp.updateDB()
        self.second = second
        self.hour = hour
        self.minute = minute
        self.update()

    def subTime(self, hour , minute , second):
        emp = employee(self.uid)
        emp.hours -= abs(datetime.timedelta(0 , second , 0 , 0 , minute , hour , 0).seconds - datetime.timedelta(
            0 , self.second , 0 , 0 , self.minute , self.hour , 0).seconds)
        emp.updateDB()
        self.second = second
        self.hour = hour
        self.minute = minute
        self.update()

    def adjustTime(self, hour , minute ,second):
        if self.action == 1 or self.action == 5:
            if datetime.timedelta(0 , second , 0 , 0 , minute , hour , 0) > datetime.timedelta(0 , self.second , 0 , 0 , self.minute , self.hour , 0):
                self.addTime(hour , minute , second)

            elif datetime.timedelta(0 , second , 0 , 0 , minute , hour , 0) < datetime.timedelta(0 , self.second , 0 , 0 , self.minute , self.hour , 0):
                self.subTime(hour , minute , second)

        elif self.action == 6 or self.action == 4 :
            if datetime.timedelta(0 , second , 0 , 0 , minute , hour , 0) > datetime.timedelta(0 , self.second , 0 , 0 ,self.minute , self.hour ,0) :
                self.subTime(hour , minute , second)

            elif datetime.timedelta(0 , second , 0 , 0 , minute , hour , 0) < datetime.timedelta(0 , self.second , 0 , 0 , self.minute , self.hour , 0) :
                self.addTime(hour , minute , second)


    @classmethod
    def getDay(cls , month , day , uid):
        try:
            return dbi('SELECT * FROM log WHERE uid = "' + str(uid) + '" AND day = ' + str(day) + ' AND month = ' + str(month) + ';')

        except:
            print('error in getDay function, mabey empty table')


    @classmethod
    def addEntry(cls , action , hours , uid , dtime):
        dbi('INSERT INTO log (month , day , hour , minute , second , hours , action , uid) values (' + str(dtime.month) +
            ' , ' + str(dtime.day) + ' , ' + str(dtime.hour) + ' , ' + str(dtime.minute) + ' , ' + str(dtime.second) + ' , ' + str(hours) +
            ' , ' + str(action) + ' , "' + str(uid) + '");')
        db.commit()


#hadles employee database
class employee:
    def __init__(self, uid):
        self.id = uid
        self.name = (dbi('SELECT name FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.totalHours = (dbi('SELECT totalHours FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.overtime = (dbi('SELECT overtime FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.hours = (dbi('SELECT hours FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.onTen = (dbi('SELECT onTen FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.onLunch = (dbi('SELECT onLunch FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.clockedIn = (dbi('SELECT clockedIn FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0]
        self.format = '%Y-%m-%d %H:%M:%S'
        self.over = datetime.timedelta(0,0,0,0,0,8)
        self.overweek = datetime.timedelta(0,0,0,0,0,40)
        self.lastTime = datetime.datetime.strptime((dbi('SELECT lastTime FROM employees WHERE uid = ' + str(self.id) + ';')).fetchall()[0][0], self.format)

    @classmethod
    def newEmployee(cls , name , uid):
        temp = datetime.datetime.now()
        dbi('INSERT INTO employees (name , lastTime , uid) values ("' + name + '" , "' + temp.strftime('%Y-%m-%d %H:%M:%S') + '" , "' + uid + '");')
        db.commit()

    @classmethod
    def listEmployees(cls):
        return dbi('SELECT uid FROM employees;')


    def updateDB(self):
        dbi('UPDATE employees SET name = "' +str(self.name) + '" ,  totalHours = "' + str(self.totalHours) +
            '" , overtime = "' + str(self.overtime) + '" , hours = "' + str(self.hours) + '" , onTen  = ' + str(self.onTen) +
            ', onLunch = ' + str(self.onLunch) + ', clockedIn = ' + str(self.clockedIn) + ' , lastTime = "' +
             self.lastTime.strftime(self.format) + '" WHERE uid = ' + str(self.id) + ';')
        db.commit()


    def clockIn(self):
        if not self.clockedIn:
            if datetime.datetime.now().day != self.lastTime.day:
                self.hours = 0
            self.lastTime = datetime.datetime.now()
            log.addEntry(1 , 0 , self.id , self.lastTime)
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
            log.addEntry(2 , temp , self.id , self.lastTime)
            self.updateDB()


    def endTen(self):
        if self.onTen:
            temp = datetime.timedelta(0,600)
            temp2 = datetime.datetime.now() - self.lastTime
            self.lastTime = datetime.datetime.now()
            if temp2 <= temp:
                self.hours += temp2.seconds
                self.totalHours += temp2.seconds
                log.addEntry(3 , temp2.seconds , self.id , self.lastTime)
            else:
                self.hours += temp.seconds
                self.totalHours += temp.seconds
                log.addEntry(3 , temp.seconds , self.id , self.lastTime)
            self.onTen = 0
            self.updateDB()


    def startLunch(self):
        if (not self.onTen) and self.clockedIn  and (not self.onLunch):
            temp = (datetime.datetime.now() - self.lastTime).seconds
            self.hours += temp
            self.totalHours += temp
            self.onLunch = 1
            self.lastTime = datetime.datetime.now()
            log.addEntry(4 , temp , self.id , self.lastTime)
            self.updateDB()



    def endLunch(self):
        if self.onLunch:
            self.lastTime = datetime.datetime.now()
            log.addEntry(5 , 0 , self.id , self.lastTime)
            self.onLunch = 0
            self.updateDB()


    def clockOut(self):
        if self.clockedIn and (not self.onLunch) and (not self.onTen):
            temp = datetime.datetime.now() - self.lastTime
            self.hours += temp.seconds
            self.totalHours += temp.seconds
            self.lastTime = datetime.datetime.now()
            log.addEntry(6 , temp.seconds , self.id , self.lastTime)
            if self.hours > self.over.seconds:
                self.overtime += self.hours - self.over.seconds
            if self.totalHours > (self.overweek.seconds + self.overtime):
                self.overtime += self.totalHours - (self.overweek.seconds + self.overtime)
            self.clockedIn = 0
            self.updateDB()


    def destroy(self):
        dbi('DELETE FROM employees WHERE uid = "' + self.id + '";')
        db.commit()
