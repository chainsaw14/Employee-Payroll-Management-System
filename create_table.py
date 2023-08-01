import mysql.connector as sql
from pwinput import pwinput
from datetime import date as d
import os
import subprocess
a=d.today()
sy=str(a.year%100)
conn = sql.connect(host='localhost', user='root', password='root')
cur=conn.cursor()
a=[]
flag=0
while(flag==0):
    a.extend([input("Enter the admin user name\n"),input("Enter the owner name\n"),pwinput("Enter the passwoed\n")])
    b=pwinput("Enter the passwoed to conform\n")
    if a[2]==b:
        db="CREATE DATABASE payroll"
        cur.execute(db)
        db='use payroll;'
        cur.execute(db)
        emp_details="create table emp_details(empID varchar(12),fname varchar(20) not null,lname varchar(20) not null,basesalary Double not null,primary key (empID),check(basesalary>9999));"
        cur.execute(emp_details)
        overtime="create table overtime (count int,month int,year int,incriment double,OvertimeID varchar(12),foreign key(overtimeID) references emp_details(empID),primary key(OvertimeID,month),check(count>=0 or count=NULL),check(incriment>=0 or incriment=NULL),check(month>0 and month<=12),check(year>2022));"
        cur.execute(overtime)
        cas_leaves="create table cas_leaves(casID varchar(12) not null,sdate date not null,edate date not null,decr double ,check (decr>=0 or decr=null),foreign key(casID) references emp_details(empID),primary key(casID,sdate));"
        cur.execute(cas_leaves)
        med_leaves="create table med_leaves(medID varchar(12),sdate date,edate date not null,decr double,check (decr>=0 or decr=null),count int,check (count>0),foreign key(medID) references emp_details(empID),primary key(medID,sdate));"
        cur.execute(med_leaves)
        salary_paid="create table salary_paid(empID varchar(12),month int not null,year int not null,salary_paid double not null,check(month>0 and month<=12),check(year>1999 and year<9999),check(salary_paid>0),foreign key(empID) references emp_details(empID),primary key(empID,month,year));"
        cur.execute(salary_paid)
        admin_log="create table admin_log(usr varchar(25) not null,owner_name varchar(25),passwd varchar(25) not null,primary key(usr));"
        cur.execute(admin_log)
        emp_log="create table emp_log(usr varchar(12) not null,owner_name varchar(25),passwd varchar(25) not null,foreign key(usr) references emp_details(empID),primary key(usr));"
        cur.execute(emp_log)
        s="insert into admin_log values(%s,%s,%s)"
        cur.execute(s,a)
        conn.commit()
        flag=1
        a.clear()
        a.extend([sy+"AHPS1",input("Enter the first name of employee\n"),input("Enter the last name of employee\n"),float(input("Enter the basic salary\n"))])
        s="insert into emp_details values(%s,%s,%s,%s)"
        cur.execute(s,a)
        conn.commit()
        s="insert into emp_log values(%s,%s,%s)"    
        x=0
        while x==0:
            del a[1:]
            a.append(input("Enter the ownername"))
            a.append(input("Enter the password for Employee login:\n"))
            if a[2]==input("Enter the password again\n"):
                cur.execute(s,a)
                conn.commit()
                x=1
            else:
                print("Wrong password\n")
        command=['python',"C:\\Users\\Pruthviraj\\OneDrive\\Desktop\\new\\main_code.py"]
        subprocess.call(command)
        os._exit(0)
    else:
        print("Something went wrong try again")
        a.clear()
