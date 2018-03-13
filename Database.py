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
    dbi('CREATE TABLE employees (id integer NOT NULL PRIMARY KEY AUTOINCREMENT,name varchar NOT NULL,'
         'totalHours smallint NOT NULL DEFAULT 0,overtime smallint NOT NULL DEFAULT 0,hours smallint NOT NULL DEFAULT 0,'
         'onTen boolean NOT NULL DEFAULT 0,onLunch boolean NOT NULL DEFAULT 0,clockedIn boolean NOT NULL DEFAULT 0,'
         'lastTime varchar NOT NULL DEFAULT 0);')

#hadles employee information
class employee:
    def __init__(self, Id):
        self.id = Id
        self.name = (dbi('SELECT name FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.totalHours = (dbi('SELECT totalHours FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.overtime = (dbi('SELECT overtime FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.hours = (dbi('SELECT hours FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.onTen = (dbi('SELECT onTen FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.onLunch = (dbi('SELECT onLunch FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.clockedIn = (dbi('SELECT clockedIn FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0]
        self.format = '%Y-%m-%d %H:%M:%S'
        self.over = datetime.timedelta(0,0,0,0,0,8)
        self.overweek = datetime.timedelta(0,0,0,0,0,40)
        self.lastTime = datetime.datetime.strptime((dbi('SELECT lastTime FROM employees WHERE id = ' + str(self.id) + ';')).fetchall()[0][0], self.format)

    @classmethod
    def newEmployee(self , name):
        temp = datetime.datetime.now()
        dbi('INSERT INTO employees (name , lastTime) values ("' + name + '" , "' + temp.strftime('%Y-%m-%d %H:%M:%S') + '");')
        db.commit()

    def updateDB(self):
        dbi('UPDATE employees SET name = "' +str(self.name) + '" ,  totalHours = "' + str(self.totalHours) +
            '" , overtime = "' + str(self.overtime) + '" , hours = "' + str(self.hours) + '" , onTen  = ' + str(self.onTen) +
            ', onLunch = ' + str(self.onLunch) + ', clockedIn = ' + str(self.clockedIn) + ' , lastTime = "' +
             self.lastTime.strftime(self.format) + '" WHERE id = ' + str(self.id) + ';')
        db.commit()

    def clockIn(self):
        if not self.clockedIn:
            if datetime.datetime.now().day != self.lastTime.day:
                self.hours = 0
            self.lastTime = datetime.datetime.now()
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
            self.updateDB()


    def startLunch(self):
        if (not self.onTen) and self.clockedIn  and (not self.onLunch):
            temp = (datetime.datetime.now() - self.lastTime).seconds
            self.hours += temp
            self.totalHours += temp
            self.onLunch = 1
            self.lastTime = datetime.datetime.now()
            self.updateDB()

    def endTen(self):
        if self.onTen:
            temp = datetime.timedelta(0,600)
            temp2 = datetime.datetime.now() - self.lastTime
            self.lastTime = datetime.datetime.now()
            if temp2 <= temp:
                self.hours += temp2.seconds
                self.totalHours += temp2.seconds
            else:
                self.hours += temp.seconds
                self.totalHours += temp.seconds
            self.onTen = 0
            self.updateDB()

    def endLunch(self):
        if self.onLunch:
            self.lastTime = datetime.datetime.now()
            self.onLunch = 0
            self.updateDB()

    def clockOut(self):
        if self.clockedIn and (not self.onLunch) and (not self.onTen):
            temp = datetime.datetime.now() - self.lastTime
            self.hours += temp.seconds
            self.totalHours += temp.seconds
            if self.hours > self.over.seconds:
                self.overtime += self.hours - self.over.seconds
            if self.totalHours > (self.overweek.seconds + self.overtime):
                self.overtime += self.totalHours - (self.overweek.seconds + self.overtime)
            self.clockedIn = 0
            self.updateDB()
