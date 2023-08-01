import mysql.connector as sql
from datetime import date as dd, datetime as d, timedelta as t
from pwinput import pwinput
import calendar
conn = sql.connect(host='localhost', user='root', password='root',database='payroll')
class emp:
    cur=conn.cursor()
    def login(self):
        self.euse = input("Enter the login id:").upper()
        passw = pwinput("Enter the password:")
        s='select usr,passwd from emp_log where usr=%(a)s'
        self.cur.execute(s,{'a':self.euse})
        result=self.cur.fetchall()
        if result !=[] and result[0][1]==passw:
                print("Login succesful...!!")
                self.chose()
        else:
                print("Login Fail...!\nTry again")
                return False
    def display(self):
        print(self.euse)
        s='select * from emp_details where empID=%(id)s'
        self.cur.execute(s,{'id':self.euse})
        result=self.cur.fetchall()
        print(result)
        print("Employee ID-",result[0][0])
        print("First Name of employee-",result[0][1])
        print("Last name of employee-",result[0][2])
        print("Basic salary of employee-",result[0][3])
    def display_sal(self):
        flag=0
        k="select * from salary_paid where empid=%(x)s and month=%(y)s and year=%(z)s"
        while flag==0:
            year=int(input("Enter the year:\n"))
            month=int(input("Enter the month number:\n"))
            self.cur.execute(k,{'x':self.euse,'y':month,'z':year})
            res=self.cur.fetchall()
            if res==[]:
                print("Details not found")
            else:
                flag=1
                print("The details Exist..!")
                print("Employee ID: ",res[0][0])
                print("Mont and year:",calendar.month_name[res[0][1]]," ",res[0][2])
                print("Final Salary:",res[0][3])
    def chose(self):
            flag=1
            while(flag!=0):
                ch=int(input("1.Display Details\n2.Display Salary details\n3.Exit\n"))
                if(ch==1):
                    self.display()
                elif(ch==2):
                    self.display_sal()
                elif ch==3:
                    flag=0
                else:
                    print("Enter correct choice\n")
class admin():
    cur=conn.cursor()
    def admlogin(self):
        ause = input("Enter the login id:")
        passw = pwinput("Enter the password:")
        s="select * from admin_log;"
        self.cur.execute(s)
        result=self.cur.fetchall()
        for res in result :
            if res[0]==ause and res[2]==passw :
                print(res[0])
                print(res[2])
                print('Employee Login successful')
                admin().choice()
            else:
                print("Login Fail...!\nTry again")
                return False
    def create_empid(self,temp):
        a=[]
        flag=0
        while(flag==0):
                a.extend([temp,input("Enter the owner_name\n"),pwinput("Enter the password \n")])
                b=pwinput("Enter the password again\n")
                if a[2]==b:
                    flag=1
                    s="insert into emp_log values(%s,%s,%s)"
                    self.cur.execute(s,a)
                    conn.commit()
               
    def create_admid(self):
          a=[]
          flag=0
          while (flag==0):
                a.extend([input("Enter the admin id to be create\n"),input("Enter the owner name\n"),pwinput("Enter the password \n")])
                b=input("Enter the password again\n")
                if a[2]==b:
                    s="insert into admin_log values(%s,%s,%s)"
                    try:
                        self.cur.execute(s,a)
                        conn.commit()
                    except sql.errors.IntegrityError:
                        print('Employee ID canot be repeted\n')
                    else:
                        flag=1
    def add_emp_details(self):
            a=dd.today()
            sy=str(a.year%100)
            a=[]
            s="select max(empID) from emp_details"
            cur=conn.cursor()
            cur.execute(s)
            result=cur.fetchall()
            temp=sy+"AHPS"+str((int(result[0][0][6:])+1))
            if str(result[0][0])!='None':
                a.extend([temp,input("Enter the first name of employee\n"),input("Enter the last name of employee\n"),float(input("Enter the basic monthly salary\n"))])
                s="insert into emp_details values(%s,%s,%s,%s)"
                cur.execute(s,a)
                conn.commit()
                print("Information Added sucessfully")
                admin().create_empid(temp)
    def add_cas_leaves(self):
        flag=1
        while flag==1:
            id=input("Enter the empid\n").upper()
            k="select * from emp_details where empID=%(x)s"
            self.cur.execute(k,{'x':id})
            result=self.cur.fetchall()
            if result==[]:
                print("ID does not found")
            else:
                flag=0
        a=input("Enter the Start Date\n")
        b=input("Enter The End Date\n")
        f="%d-%m-%Y"
        st=d.strptime(a,f)
        ed=d.strptime(b,f)
        curret=st
        count=0
        k="select sdate,edate from cas_leaves where casID=%(x)s"
        self.cur.execute(k,{'x':id})
        res1=self.cur.fetchall()
        '''flag=1
        if res1==[]:
            flag=1
        else:
            for r in res1:
                if r[0]'''
        if st<ed and st.month!=ed.month:
            last=calendar.monthrange(st.year,st.month)[1]
            eed=d.strptime(str(last)+'-'+str(st.month)+'-'+str(st.year),f)
            print(eed)
            while curret<eed:
                if curret.weekday()!=6:
                    count=count+1
                curret+=t(days=1)
            dec=count*(result[0][3]/25)
            a1=[id,st.date(),eed.date(),dec]
            eed+=t(days=1)
            count=0
            a2=[id,eed.date()]
            while eed<ed:
                if eed.weekday()!=6:
                    count=count+1
                eed+=t(days=1)
            dec=count*(result[0][3]/25)
            a2.extend([ed.date(),dec])
        elif st<ed:
            flag=1
            while curret<ed:
                if curret.weekday()!=6:
                    count=count+1
                curret+=t(days=1)
            dec=count*(result[0][3]/25)
            a1=[id,st.date(),ed.date(),dec]
        else:
            print("Wrong Dates Entered")
            exit()
        s='insert into cas_leaves values(%s,%s,%s,%s)'
        if flag==0:
            try:
                self.cur.execute(s,a1)
                conn.commit()
                self.cur.execute(s,a2)
                conn.commit()
            except sql.errors.IntegrityError:
                print("Invalid Dates Try again")
        else:
            try:
                self.cur.execute(s,a1)
                conn.commit()
            except sql.errors.IntegrityError:
                print("Invalid dates try again")
    def add_med_leaves(self):
        flag=1
        x=0
        while flag==1:
            id=input("Enter the empid\n").upper()
            k="select * from emp_details where empID=%(x)s"
            self.cur.execute(k,{'x':id})
            result=self.cur.fetchall()
            if result==[]:
                print("ID does not found")
            else:
                flag=0
            k="select * from med_leaves where medID=%(x)s"
            self.cur.execute(k,{'x':id})
            result1=self.cur.fetchall()
            if result1!=[]:
                for res in result1:
                    x=x+res[4]
        s='insert into med_leaves values(%s,%s,%s,%s,%s)'
        a=input("Enter the Start Date\n")
        b=input("Enter The End Date\n")
        f="%d-%m-%Y"
        st=d.strptime(a,f)
        ed=d.strptime(b,f)
        curret=st
        count=0
        z=4
        if st<ed and st.month!=ed.month:
            last=calendar.monthrange(st.year,st.month)[1]
            eed=d.strptime(str(last)+'-'+str(st.month)+'-'+str(st.year),f)
            print(eed)
            while curret<=eed:
                if curret.weekday()!=6:
                    count=count+1
                curret+=t(days=1)
            if z-x>0:
                z=z-x
            else:
                z=0
            if count<z:
                dec=0
                z=z-count
            else:
                dec=(count-z)*(result[0][3]/60)
                z=0
            x=x+count
            a1=[id,st.date(),eed.date(),dec,count]
            eed+=t(days=1)
            count=0
            a2=[id,eed.date()]
            while eed<ed:
                if eed.weekday()!=6:
                    count=count+1
                eed+=t(days=1)
            if z-x>0:
                z=z-x
            else:
                z=0
            if count<z:
                dec=0
                z=z-count
            else:
                dec=(count-z)*(result[0][3]/60)
            a2.extend([ed.date(),dec,count])
        elif st<ed:
            flag=1
            while curret<ed:
                if curret.weekday()!=6:
                    count=count+1
                    print(count)
                curret+=t(days=1)
            if z-x>0:
                z=z-x
            else:
                z=0
            if count<z:
                dec=0
            else:
                dec=(count-z)*(result[0][3]/60)
            a1=[id,st.date(),ed.date(),dec,count]
        else:
            print("Wrong Dates Entered")
            exit()

        if flag==0:
            try:
                self.cur.execute(s,a1)
                conn.commit()
                self.cur.execute(s,a2)
                conn.commit()
            except sql.errors.IntegrityError:
                print("Invalid Dates Try again")
        else:
            try:
                self.cur.execute(s,a1)
                conn.commit()
            except sql.errors.IntegrityError:
                print("Invalid dates try again")
    def add_overtime(self):
        flag=1
        while flag==1:
            id=input("Enter the empid\n").upper()
            k="select * from emp_details where empID=%(x)s"
            self.cur.execute(k,{'x':id})
            result=self.cur.fetchall()
            if result==[]:
                print("ID does not found")
            else:
                flag=0
        month=int(input("Enter the month number\n"))
        year=int(input("Enter the year number\n"))
        count=int(input("Enter the number of hours for a month\n"))
        inc=count*(result[0][3]/200)
        a=[count,month,year,inc,id]
        k="insert into overtime values(%s,%s,%s,%s,%s)"
        self.cur.execute(k,a)
        conn.commit()
    def add_salary_paid(self):
        flag=1
        while flag==1:
            id=input("Enter the empid\n").upper()
            k="select * from emp_details where empID=%(x)s"
            self.cur.execute(k,{'x':id})
            result=self.cur.fetchall()
            if result==[]:
                print("ID does not found")
            else:
                flag=0
            month=int(d.now().month)
            year=int(d.now().year)
            k="select * from salary_paid where empid=%(x)s and month=%(y)s and year=%(z)s"
            self.cur.execute(k,{'x':id,'y':month,'z':year})
            res=self.cur.fetchall()
            if res==[]:
                k="select incriment from overtime where OvertimeID=%(x)s and month=%(y)s"
                self.cur.execute(k,{'x':id,'y':month})
                over=self.cur.fetchall()
                if over==[]:
                    over.append([0])
                k="select decr,sdate from cas_leaves where casID=%(x)s having(month(sdate)=%(z)s and year(sdate)=%(y)s)"
                self.cur.execute(k,{'x':id,'z':month,'y':year})
                cas=self.cur.fetchall()
                if cas==[]:
                    cas.append([0])
                k="select decr,sdate from med_leaves where medID=%(x)s having(month(sdate)=%(z)s and year(sdate)=%(y)s)"
                self.cur.execute(k,{'x':id,'z':month,'y':year})
                med=self.cur.fetchall()
                if med==[]:
                    med.append([0])
                salary_paid=(over[0][0]+result[0][3])-((sum(sublist[0] for sublist in cas))+(sum(sublist[0] for sublist in med)))
                a=[id,month,year,salary_paid]
                k="insert into salary_paid values(%s,%s,%s,%s)"
                self.cur.execute(k,a)
                conn.commit()
                print("The details added successfully.....!")
            else:
                print("The details Exist..!")
                print("Employee ID: ",res[0][0])
                print("Mont and year:",calendar.month_name[res[0][1]]," ",res[0][2])
                print("Final Salary:",res[0][3])
    def choice(self):
        flag=0
        while(flag!=1):
            co=int(input('Enter Your choice:\n1.Add new admin login\n2.Add New Employee details\n3.Add the casual leaves\n4.Add medical leaves\n5.Add Overtime\n6.Add Salary Details\n7.Exit\n'))
            if co==1:
                self.create_admid()
            elif co==2:
                self.add_emp_details()
            elif co==3:
                self.add_cas_leaves()
            elif co==4:
                self.add_med_leaves()
            elif co==5:
                self.add_overtime()
            elif co==6:
                self.add_salary_paid()
            elif co==7:
                flag=1
            else:
                print("Wrong choice")
flag=0
while(flag!=1):
    ch=int(input("Choose the type of login\n1.Employee\n2.Payroll Manager\n3.Exit\n"))
    if ch==1:
        obj=emp
        obj().login()
    elif ch==2:
        obj1=admin
        obj1().admlogin()
    elif ch==3:
        flag=1
    else:
        print('Wrong choice....!!\n')