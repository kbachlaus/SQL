#CS4400 Database Project
#GT Medical Records System (GTMRS)
import tkinter
from tkinter import *
import pymysql
from datetime import datetime, timedelta
import time

class GTMRS:

    def __init__(self,window):
        self.Window= window
        self.Window.withdraw()
        self.LoggingIn()
        self.Entries=()
        self.Availability=()
        self.medicationList =[]
        self.listVerification = []
        
    def LoggingIn(self):
        self.root= Toplevel()
        self.root.title("Login")
        
##        self.photo= PhotoImage(file="buzz1.bmp")
##        self.root.l= Label(self.root, image=self.photo)
##        self.root.l.photo= self.photo
##        self.root.l.grid(row=0, column=0, columnspan=3)
        
        self.root.l1= Label(self.root, text='Username:')
        self.root.l1.grid(row=2, column=0, sticky=E)
        
        self.root.e1= Entry(self.root, width= 50, state=NORMAL)
        self.root.e1.grid(row=2, column=1)
        
        self.root.l2= Label(self.root, text="Password:")
        self.root.l2.grid(row=3, column=0, sticky=E)
        
        self.root.e2= Entry(self.root, width=50, state=NORMAL)
        self.root.e2.grid(row=3, column=1)

        self.root.l3= Label(self.root, text="")
        self.root.l3.grid(row=3, column=0, sticky=E)
        
        self.root.b1= Button(self.root, text="Register", command=self.Register)
        self.root.b1.grid(row=4, column=1, sticky=E)
        
        self.root.b2= Button(self.root, text="Login",command=self.LoginCheck)
        self.root.b2.grid(row=4, column=2)

    def Register(self):
        self.root.withdraw()

        self.root2= Toplevel()
        self.root2.title('New User Registration')      
        
        self.root2.l2= Label(self.root2, text="Username:")
        self.root2.l2.grid(row=1, column=0, sticky=W)
        
        self.root2.e2= Entry(self.root2, width=50, state=NORMAL)
        self.root2.e2.grid(row=1, column=1)

        self.root2.l3= Label(self.root2, text='Password:')
        self.root2.l3.grid(row=2, column=0, sticky=W)
        
        self.root2.e3= Entry(self.root2, width= 50, state=NORMAL)
        self.root2.e3.grid(row=2, column=1)
        
        self.root2.l4= Label(self.root2, text="Confirm Password:")
        self.root2.l4.grid(row=3, column=0, sticky=W)
    
        self.root2.e4= Entry(self.root2, width=50, state=NORMAL)
        self.root2.e4.grid(row=3, column=1)

        self.root2.l6= Label(self.root2, text="Type of User:")
        self.root2.l6.grid(row=4, column=0)

        self.var1 = tkinter.StringVar(self.root2)
        self.var1.set('Doctor')
        choices = ['Doctor','Patient','Admin']
        self.root2.option = tkinter.OptionMenu(self.root2, self.var1, *choices)
        self.root2.option.grid(row=4, column=1)
                    
        print('hi')
        self.root2.b1= Button(self.root2, text="Cancel", command=self.Cancel)
        self.root2.b1.grid(row=6, column=0)
        print('hello')
        self.root2.b2= Button(self.root2, text="Create Account",command=self.CreateAccount)
        self.root2.b2.grid(row=6, column=1)
        print('yo')

    def Cancel(self):
        #helper function
        self.root2.withdraw()
        self.LoggingIn() #will it not work if the main level is withdrawn?

    def Connect(self):
        try:
            db = pymysql.connect(host='academic-mysql.cc.gatech.edu', passwd='Xd6Ff4z2', user='cs4400_Group_59', db='cs4400_Group_59')
            print ("it worked. db connected to CS4400 Database")
            return db
        except:
            result=messagebox.showwarning("Database cannot connect","Check your internet connection")
            print("god...why isn't this working :_( ")

    def CreateAccount(self):
    
        self.Username= self.root2.e2.get()
        self.Password= self.root2.e3.get()
        self.ConfirmPassword= self.root2.e4.get()
        #Gets the information from the entry boxes
        self.root2.USERchosen= self.var1.get() #value of drop down user type

        if self.Username=='':
            messagebox.showerror("Username","Please enter a username.")     
        if self.Password=='':
            messagebox.showerror("Password","Please enter a password.")
        if self.ConfirmPassword=='':
            messagebox.showerror("ConfirmPassword","Please enter the same password.")
        elif self.Password==self.ConfirmPassword:
            print('Same Password. Allow connection')
        else:
            messagebox.showerror("Password","Passwords do not match. Please try again.")

        #ENTER DROP DOWN OPTION FOR TYPE OF USER
        #save chosen option into a variable (used later to decide which profile to create)
        db= self.Connect()
        sql= "SELECT * FROM USER WHERE username=%s"
        c=db.cursor()
        c.execute(sql, (self.Username)) #second argument is a tuple, even if it is one element
        db.commit

        ListUsers=[]
        for item in c:
            ListUsers.append(item)            
        
        #Data Available:
        if len(ListUsers)!=0:
            messagebox.showerror("Username Taken", "Please select another username")
            GO= False
        else:
            GO= True
        
        c.close()
        db.close()
            
        if GO==True:
            db = self.Connect()
            sql= "INSERT INTO USER(Username, Password) VALUES (%s,%s)"
            c=db.cursor()
            c.execute(sql, (self.Username,self.Password) )
            db.commit()
            c.close()
            db.close()

            messagebox.showwarning("Registered", "User has now been registered")

            self.root2.withdraw()
            self.UserType=self.root2.USERchosen
            
            if self.root2.USERchosen=='Doctor':
                self.CreateDocProfile()
            elif self.root2.USERchosen=='Patient':
                self.PaymentInformation()
            else:
                pass
            
    def LoginCheck(self):

        self.Username1= self.root.e1.get()
        self.Username= self.Username1
        self.Password1= self.root.e2.get()
        #Gets the information from the entry boxes
        
        DB= self.Connect()
        sql= 'SELECT * FROM USER WHERE USER.Username = %s AND USER.Password = %s'
        c= DB.cursor()
        c.execute(sql, (self.Username1,self.Password1) )
        DB.commit()

        c.close
        DB.close()
        ITEMS=[]
        for item in c:
            print(item)
            ITEMS.append(item)        

        if len(ITEMS)==0:
            messagebox.showerror("No Match Found", "Unrecognizable username/password used. Please try again")
        elif len(ITEMS)==1:
            if ITEMS[0][1]==self.Password1:
                messagebox.askquestion("Login Successful", "You have logged in successfully")
                self.root.withdraw()

                db= self.Connect()
                sql= "SELECT PatientUsername From Patient WHERE Patient.PatientUsername = %s"
                c=db.cursor()
                c.execute(sql, (self.Username,)) #second argument is a tuple, even if it is one element
                db.commit

                ListA=[]
                for item in c:
                    ListA.append(item)
                l=len(ListA)
                if l==0:            
                    db= self.Connect()
                    sql= "SELECT DocUsername From Doctor WHERE Doctor.DocUsername = %s"
                    c=db.cursor()
                    c.execute(sql, (self.Username,)) #second argument is a tuple, even if it is one element
                    db.commit

                    ListB=[]
                    for item in c:
                        ListB.append(item)
                        l=len(ListB)
                        if l==0:
                            self.UserType='Admin'
                            print(self.UserType)
                            #call Admin HOmepage
                        else:
                            self.UserType='Doctor'
                            #self.DoctorHomepage()
                            print(self.UserType)
                else:
                    self.UserType='Patient'
                    self.PatientHomepage()
                
        else:
            messagebox.showwarning("Invalid", "More than one registration in database!")
            self.root2.destroy()
            

    def CreateDocProfile(self): #NEED MAJOR HELP
        self.root2.withdraw()

        self.root3= Toplevel()
        self.root3.title('Doctor Profile')

        self.root3.l1= Label(self.root3, text="License Number:")
        self.root3.l1.grid(row=0, column=0)
        self.root3.e1= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e1.grid(row=0, column=1)

        self.root3.l2= Label(self.root3, text="First Name:")
        self.root3.l2.grid(row=1, column=0)
        self.root3.e2= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e2.grid(row=1, column=1)

        self.root3.l3= Label(self.root3, text="Last Name:")
        self.root3.l3.grid(row=2, column=0)
        self.root3.e3= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e3.grid(row=2, column=1)

        self.root3.l4= Label(self.root3, text="Date of Birth:")
        self.root3.l4.grid(row=3, column=0)
        self.root3.e4= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e4.grid(row=3, column=1)

        self.root3.l5= Label(self.root3, text="Work Phone")
        self.root3.l5.grid(row=4, column=0)
        self.root3.e5= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e5.grid(row=4, column=1)

        self.root3.l6= Label(self.root3, text="Speciality")
        self.root3.l6.grid(row=5, column=0)

        self.var3 = tkinter.StringVar(self.root3)
        self.var3.set('Heart Specialist')
        choices3 = ['Heart Specialist','Eye Physician','General Physician','Orthopedics','Psychiatry','Gynecologist']
        option3 = tkinter.OptionMenu(self.root3, self.var3, *choices3)
        option3.grid(row=5, column=1)

        self.root3.l7= Label(self.root3, text="Room Number")
        self.root3.l7.grid(row=6, column=0)
        self.root3.e7= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e7.grid(row=6, column=1)

        self.root3.l8= Label(self.root3, text="Home Address")
        self.root3.l8.grid(row=7, column=0)
        self.root3.e8= Entry(self.root3, width=60, state=NORMAL)
        self.root3.e8.grid(row=7, column=1)

        self.root3.l9= Label(self.root3, text="Availability")
        self.root3.l9.grid(row=8, column=0)

        self.var4 = tkinter.StringVar(self.root3)
        self.var4.set('Monday')
        choices4 = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        option4 = tkinter.OptionMenu(self.root3, self.var4, *choices4)
        option4.grid(row=8, column=1)

        self.root3.l10= Label(self.root3, text="From")
        self.root3.l10.grid(row=8, column=2)

        self.var5 = tkinter.StringVar(self.root3)
        self.var5.set('07:00')
        choices5 = ['07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']
        option5 = tkinter.OptionMenu(self.root3, self.var5, *choices5)
        option5.grid(row=8, column=3)

        self.root3.l11= Label(self.root3, text="To")
        self.root3.l11.grid(row=8, column=4)

        self.var6 = tkinter.StringVar(self.root3)
        self.var6.set('07:00')
        choices6 = ['07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']
        option6 = tkinter.OptionMenu(self.root3, self.var6, *choices6)
        option6.grid(row=8, column=5)

        self.root3.b1= Button(self.root3, text="+", command=self.AddAppointments)
        self.root3.b1.grid(row=8, column=6)

        self.root3.b2= Button(self.root3, text="Submit",command=self.DocSubmit)
        self.root3.b2.grid(row=0, column=3)

        self.f1=Frame(self.root3)
        self.f1.grid(row=9, column=0)        

    def AddAppointments(self): #LOOK OVER AGAIN - CRASHING
        self.Availability= self.Availability+(self.var4.get(), self.var5.get(), self.var6.get())
        
        self.group = LabelFrame(self.f1, text="And", padx=5, pady=5)
        self.group.pack(padx=10, pady=10)

        self.root3.l1= Label(self.group, text="Availability")
        self.root3.l1.pack(side=LEFT)

        self.var4 = tkinter.StringVar(self.group)
        self.var4.set('Monday')
        choices = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        option = tkinter.OptionMenu(self.group,self.var4, *choices)
        option.pack(side=LEFT)
                    
        self.root3.l2= Label(self.group, text="From")
        self.root3.l2.pack(side=LEFT)
        
        self.var5 = tkinter.StringVar(self.group)
        self.var5.set('07:00')
        choices = ['07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']
        option = tkinter.OptionMenu(self.group, self.var5, *choices)
        option.pack(side=LEFT) 

        self.root3.l3= Label(self.group, text="To")
        self.root3.l3.pack(side=LEFT) 
            
        self.var6 = tkinter.StringVar(self.group)
        self.var6.set('07:00')
        choices = ['07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00']
        option = tkinter.OptionMenu(self.group, self.var6, *choices)
        option.pack(side=LEFT)

        #self.DocSubmit()
                    
    def DocSubmit(self):
        self.Availability= self.Availability+((self.var4.get(), self.var5.get(), self.var6.get()),)
        print(self.Availability)

        #maybe need more sql statements to enter info from other entry boxes
        db= self.Connect()
        sql= "INSERT INTO Doctor(DocUsername, LicenseNo, FName, LName, DOB, WorkPhone, RoomNo, HomeAddress, Specialty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        c=db.cursor()
        c.execute(sql, (self.Username, self.root3.e1.get(), self.root3.e2.get(), self.root3.e3.get(),self.root3.e4.get(), self.root3.e5.get(),self.root3.e7.get(), self.root3.e8.get(), self.var3.get()) )

        for i in self.Availability :
            sql= "INSERT INTO Doctor_Availability (DocUsername, Day, From, To) VALUES (%s ,%s, %s, %s)"
            c=db.cursor()
            c.execute(sql,(self.Username, i[0], i[1], i[2]))
        
        db.commit
        c.close()
        db.close()
        
    
    
    def CreatePatProfile(self):
     
        self.root4= Toplevel()
        self.root4.title('Patient Profile')

        self.root4.l1= Label(self.root4, text="Patient Name:")
        self.root4.l1.grid(row=1, column=0, sticky=W)
        
        self.root4.e1= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e1.grid(row=1, column=1)

        self.root4.l2= Label(self.root4, text="Date of Birth:")
        self.root4.l2.grid(row=2, column=0, sticky=W)

        self.root4.e2= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e2.grid(row=2, column=1)

        self.root4.l3= Label(self.root4, text="Gender:")
        self.root4.l3.grid(row=3, column=0, sticky=W)

        self.var2 = tkinter.StringVar(self.root4)
        self.var2.set('Male')
        choices2 = ['Male', 'Female']
        option2 = tkinter.OptionMenu(self.root4, self.var2, *choices2)
        option2.grid(row=3, column=1)      

        self.root4.l4= Label(self.root4, text="Address:")
        self.root4.l4.grid(row=4, column=0, sticky=W)
        
        self.root4.e4= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e4.grid(row=4, column=1)

        self.root4.l5= Label(self.root4, text="Home Phone:")
        self.root4.l5.grid(row=5, column=0, sticky=W)
        
        self.root4.e5= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e5.grid(row=5, column=1)

        self.root4.l6= Label(self.root4, text="Work Phone:")
        self.root4.l6.grid(row=6, column=0, sticky=W)
        
        self.root4.e6= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e6.grid(row=6, column=1)

        self.root4.l7= Label(self.root4, text="Weight:")
        self.root4.l7.grid(row=7, column=0, sticky=W)
        
        self.root4.e7= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e7.grid(row=7, column=1)

        self.root4.l8= Label(self.root4, text="Height:")
        self.root4.l8.grid(row=8, column=0, sticky=W)
        
        self.root4.e8= Entry(self.root4, width=60, state=NORMAL)
        self.root4.e8.grid(row=8, column=1)
        
        self.root4.l9= Label(self.root4, text="Annual Income ($):")
        self.root4.l9.grid(row=9, column=0, sticky=W)

        self.var3 = tkinter.StringVar(self.root4)
        self.var3.set('25000- 50000')
        choices3 = ['0- 25000','25000- 50000', '50000 & above']
        option3 = tkinter.OptionMenu(self.root4, self.var3, *choices3)
        option3.grid(row=9, column=1)

        self.root4.b1= Button(self.root4, text="Submit", command= self.PatSubmit)
        self.root4.b1.grid(row=9, column=2, sticky=W)

        self.root4.l10= Label(self.root4, text="Allergies:")
        self.root4.l10.grid(row=10, column=0, sticky=W)
        print('1')
        self.entry= StringVar()
        print('2')
        self.root4.e= Entry(self.root4, width=60, textvariable=self.entry)
        print('3')
        self.root4.e.grid(row=11, column= 1)
        print('4')
        self.root4.b10= Button(self.root4, text="+ (add another allergy)", command=self.AddAllergy)
        print('5')
        self.root4.b10.grid(row=11, column=2, sticky=W)
        print('6')

        self.f=Frame(self.root4)
        self.f.grid(row=11, column=1)

    
    def AddAllergy(self): #need help with
        self.Entries=self.Entries +(self.root4.e.get(),)
        self.entry= StringVar()
        self.root4.e= Entry(self.f, width=60, state=NORMAL, textvariable=self.entry)
        self.root4.e.pack()

    def PatSubmit(self):
        self.Entries=self.Entries +(self.root4.e.get(),)
        

        #maybe need more sql statements to enter info from other entry boxes
        db= self.Connect()
        sql= "INSERT INTO Patient(PatientUsername, Name, DOB, Gender, Address,WorkPhone, HomePhone, ECPhone, ECName, Height, Weight, AnnualIncome, CardNumber) VALUES (%s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s,%s,%s)"
        c=db.cursor()
        params= (self.Username, self.root4.e1.get(), self.root4.e2.get(), self.var2.get(), self.root4.e4.get(), self.root4.e6.get(), self.root4.e5.get(),'','', self.root4.e8.get(), self.root4.e7.get(), self.var3.get(),'') 
        c.execute(sql, params ) #second argument is a tuple, even if it is one element
        db.commit

        for i in self.Entries:
            sql= "INSERT INTO Patient Allergies(PatientUsername, Allergy) VALUES (%s,%s)" 
            c=db.cursor()
            c.execute(sql,(self.Username, i)) #second argument is a tuple, even if it is one element

        c.close()
        db.close()

        self.root4.withdraw()
        self.PatientHomepage()
        

    def PatientHomepage(self):
        self.root5=Toplevel()

        self.root5.b1= Button(self.root5, text="Make Appointments", command=self.SearchAppointmentPage)
        self.root5.b1.pack()
        self.root5.b2= Button(self.root5, text="View Visit History", command=self.VisitHistory)
        self.root5.b2.pack()
        self.root5.b3= Button(self.root5, text="Order Medication", command=self.OrderMedication)
        self.root5.b3.pack()
        self.root5.b4= Button(self.root5, text="Communicate", command=self.messages)
        self.root5.b4.pack()
        self.root5.b5= Button(self.root5, text="Rate a Doctor", command=self.RateDoctor)
        self.root5.b5.pack()
        self.root5.b6= Button(self.root5, text="Edit Profile", command=self.EditProfile)
        self.root5.b6.pack()
        self.root5.b7= Button(self.root5, text="You have x unread messages", command=self.NumberofMsgs)
        self.root5.b7.pack()
        

    def SearchAppointmentPage(self):
        self.root5.withdraw()
        self.root6=Toplevel()

        f1= Frame(self.root6)
        f1.pack()
        
        self.root6.l1= Label(f1, text="Speciality:")
        self.root6.l1.grid(row=0, column=0, sticky=W)
                              
        self.var1 = tkinter.StringVar(self.root6)
        self.var1.set('Eye Physician')
        choices1 = ['Heart Specialist','Eye Physician','General Physician','Orthopedics','Psychiatry','Gynecologist']
        self.root6.option1 = tkinter.OptionMenu(f1, self.var1, *choices1)
        self.root6.option1.grid(row=0, column=1)       

        self.root6.b1= Button(f1, text="Search", command=self.SearchAppointments)
        self.root6.b1.grid(row=0, column=4, sticky=E)

    def SearchAppointments(self):
        f2= Frame(self.root6)
        f2.pack()

        self.root6.l1= Label(f2, text='Doctor FName',width=20)
        self.root6.l1.grid(row=0, column=0)
        self.root6.l1= Label(f2, text='Doctor LName',width=20)
        self.root6.l1.grid(row=0, column=1)
        self.root6.l2= Label(f2, text='Work Number',width=20)
        self.root6.l2.grid(row=0, column=2)
        self.root6.l3= Label(f2, text='Room Number',width=20)
        self.root6.l3.grid(row=0, column=3)
        self.root6.l4= Label(f2, text='Day',width=20)
        self.root6.l4.grid(row=0, column=4)
        self.root6.l1= Label(f2, text='To',width=20)
        self.root6.l1.grid(row=0, column=5)
        self.root6.l1= Label(f2, text='From',width=20)
        self.root6.l1.grid(row=0, column=6)
        self.root6.l1= Label(f2, text='Average Rating',width=20)
        self.root6.l1.grid(row=0, column=7)                     

        print(self.var1.get())

        db= self.Connect()
        sql= "SELECT d.FName, d.LName, d.WorkPhone, d.RoomNo, a.To, a.From, a.Day , AVG(r.Rating) AS Average_Rating FROM Doctor d, Doctor_Availability a , Doctor_Rating r  WHERE d.Specialty = %s AND d.DocUsername = a.DocUsername AND r.DocUsername = d.DocUsername GROUP BY r.DocUsername"
        c=db.cursor()
        c.execute(sql, (self.var1.get(),))
        c.close()
        db.close()

        self.ListDocsAvailability=[] 
        for tupe in c:
            print(tupe)
            self.ListDocsAvailability.append(tupe)

        print(self.ListDocsAvailability)
        #returns nested list of [FN, LN, WP#, RM#, TO, FROM, DAY]

        NumApp= len(self.ListDocsAvailability)
        print(NumApp)
        NumInfo= len(self.ListDocsAvailability[0]) #may get more complicated with only available appointments, and not all appointments
        #in above list, don't include average rating as info. That is derived information
        print(NumInfo)
        
        self.var= IntVar()
        self.var.set(1)
        for i in list(range(0,NumApp)): #still doesn't work completely
            f= Frame(self.root6)
            f.pack()
            A=self.ListDocsAvailability[i]
            c1= Radiobutton(f, variable=self.var, value=i)
            c1.grid(row=i, column=0)

            for j in list(range(0,NumInfo)):
                e= Entry(f)
                e.grid(row=i, column=j+1)
                e.delete(0,END)
                e.insert(0, A[j])
                e.config(state=DISABLED)
        
        f3= Frame(self.root6)
        f3.pack()

        self.root6.b2=Button(f3, text='Request Appointment', command=self.RequestAppointment)
        self.root6.b2.pack()

    def RequestAppointment(self):
        N=self.var.get()
        self.SelectedAvailabilityRow= self.ListDocsAvailability[N]

        self.DFN= self.ListDocsAvailability[N][0]
        self.DLN= self.ListDocsAvailability[N][1]
        self.WP = self.ListDocsAvailability[N][2]
        self.RM = self.ListDocsAvailability[N][3]
        self.DAY = self.ListDocsAvailability[N][4]
        self.FROM = self.ListDocsAvailability[N][5]
        self.TO = self.ListDocsAvailability[N][6]

##        db= self.Connect()
##        sql= "INSERT INTO Appointments(DocUsername, PatientUsername, Date, Time) VALUES (%s, %s, %s, %s)"
##        c=db.cursor()
##        c.execute(sql, (,self.Username,  ))
##        c.close()
##        db.close()
        self.root6.withdraw()
        self.PatientHomepage()
        
                                            
    def OrderMedication(self):
        self.root5.destroy()
        self.root7=Toplevel()
        self.root7.title('Order Medication From Pharmacy')

        self.root7.l1= Label(self.root7, text="Medicine Name:")
        self.root7.l1.grid(row=0, column=0, sticky=W)

        self.root7.e1= Entry(self.root7, width=60, state=NORMAL)
        self.root7.e1.grid(row=0, column =1)

        self.root7.l2= Label(self.root7, text="Dosage:")
        self.root7.l2.grid(row=1, column=0, sticky=W)

        self.root7.var1 = tkinter.StringVar(self.root7)
        self.root7.var1.set('1')
        choices1 = ['1','2','3','4','5']
        self.root7.option1 = tkinter.OptionMenu(self.root7, self.root7.var1, *choices1)
        self.root7.option1.grid(row=1, column=1)

        self.root7.l3= Label(self.root7, text="per day")
        self.root7.l3.grid(row=1, column=3, sticky=W)

        self.root7.l4= Label(self.root7, text="Duration:")
        self.root7.l4.grid(row=2, column=0, sticky=W)

        self.root7.var2 = tkinter.StringVar(self.root7)
        self.root7.var2.set('0')
        choices2 = ['0','1','2','3','4','5','6','7','8','9','10','11','12']
        self.root7.option2 = tkinter.OptionMenu(self.root7, self.root7.var2, *choices2)
        self.root7.option2.grid(row=2, column=1)

        self.root7.l5= Label(self.root7, text="Months")
        self.root7.l5.grid(row=2, column=2, sticky=W)
                              
        self.root7.var3 = tkinter.StringVar(self.root7)
        self.root7.var3.set('0')
        choices3 = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        self.root7.option3 = tkinter.OptionMenu(self.root7, self.root7.var3, *choices3)
        self.root7.option3.grid(row=2, column=3)

        self.root7.l6= Label(self.root7, text="Days")
        self.root7.l6.grid(row=2, column=4, sticky=W)

        self.root7.l7= Label(self.root7, text="Consulting Doctor:")
        self.root7.l7.grid(row=3, column=0, sticky=W)

        self.root7.e2= Entry(self.root7, width=60, state=NORMAL)
        self.root7.e2.grid(row=3, column =1)

        self.root7.l8= Label(self.root7, text="Date of Prescription:")
        self.root7.l8.grid(row=4, column=0, sticky=W)

        self.root7.e3= Entry(self.root7, width=60)                      
        self.root7.e3.grid(row=4, column=1)       

        self.root7.b1= Button(self.root7, text="Add medication to basket", command=self.AddToBasket)
        self.root7.b1.grid(row=5, column=4, sticky=E)

        self.root7.b2= Button(self.root7, text="Checkout", command=self.PaymentInformationTwo)
        self.root7.b2.grid(row=5, column=5, sticky=E)

    def PaymentInformation(self):
        #self.rootx.destroy()
        self.root8=Toplevel()
        self.root8.title('Payment Information')

        self.root8.l1= Label(self.root8, text="Card Holder's Name")
        self.root8.l1.grid(row=0, column=0, sticky=W)

        self.root8.e1= Entry(self.root8, width=60)                      
        self.root8.e1.grid(row=0, column=1)

        self.root8.l2= Label(self.root8, text="Card Number")
        self.root8.l2.grid(row=1, column=0, sticky=W)

        self.root8.e2= Entry(self.root8, width=60)                      
        self.root8.e2.grid(row=1, column=1)

        self.root8.l3= Label(self.root8, text="Type of Card")
        self.root8.l3.grid(row=2, column=0, sticky=W)

        self.root8.var1 = tkinter.StringVar(self.root8)
        self.root8.var1.set('Visa')
        choices1 = ['Visa','Mastercard','American Express']
        self.root8.option1 = tkinter.OptionMenu(self.root8, self.root8.var1, *choices1)
        self.root8.option1.grid(row=2, column=1)

        self.root8.l4= Label(self.root8, text="CVV:")
        self.root8.l4.grid(row=3, column=0, sticky=W)

        self.root8.e3= Entry(self.root8, width=60)                      
        self.root8.e3.grid(row=3, column=1)

        self.root8.l5= Label(self.root8, text="Date Of Expiry:")
        self.root8.l5.grid(row=4, column=0, sticky=W)

        self.root8.e4= Entry(self.root8, width=60)                      
        self.root8.e4.grid(row=4, column=1)

        self.root8.b1= Button(self.root8, text='Submit', command=self.SubmitPayInfo)
        self.root8.b1.grid(row=5, column=3)

    def SubmitPayInfo(self):

        #Insert Card Info:
        db= self.Connect()
        sql= "INSERT INTO Payment_Information VALUES (%s,%s,%s,%s,%s)"
        c=db.cursor()
        c.execute(sql, (self.root8.e2.get(),self.root8.e1.get(),self.root8.e3.get(),self.root8.var1.get(),self.root8.e4.get()))
        db.commit

        self.root8.withdraw()
        self.CreatePatProfile()


    def PaymentInformationTwo(self):
        self.root7.withdraw()
        self.root8=Toplevel()
        self.root8.title('Payment Information')

        self.root8.l1= Label(self.root8, text="Card Holder's Name")
        self.root8.l1.grid(row=0, column=0, sticky=W)

        self.root8.e1= Entry(self.root8, width=60)                      
        self.root8.e1.grid(row=0, column=1)

        self.root8.l2= Label(self.root8, text="Card Number")
        self.root8.l2.grid(row=1, column=0, sticky=W)

        self.root8.e2= Entry(self.root8, width=60)                      
        self.root8.e2.grid(row=1, column=1)

        self.root8.l3= Label(self.root8, text="Type of Card")
        self.root8.l3.grid(row=2, column=0, sticky=W)

        self.root8.var1 = tkinter.StringVar(self.root8)
        self.root8.var1.set('Visa')
        choices1 = ['Visa','Mastercard','American Express']
        self.root8.option1 = tkinter.OptionMenu(self.root8, self.root8.var1, *choices1)
        self.root8.option1.grid(row=2, column=1)

        self.root8.l4= Label(self.root8, text="CVV:")
        self.root8.l4.grid(row=3, column=0, sticky=W)

        self.root8.e3= Entry(self.root8, width=60)                      
        self.root8.e3.grid(row=3, column=1)

        self.root8.l5= Label(self.root8, text="Date Of Expiry:")
        self.root8.l5.grid(row=4, column=0, sticky=W)

        self.root8.e4= Entry(self.root8, width=60)                      
        self.root8.e4.grid(row=4, column=1)

        self.root8.b1= Button(self.root8, text='Order', command=self.OrderMeds)
        self.root8.b1.grid(row=5, column=3)

        #sql stuff now:
        db= self.Connect()
        sql= "SELECT p.CardNumber, p.CardholdersName, p.CCV, p.DOE, p.Type FROM Payment_Information AS p, Patient WHERE Patient.CardNumber=p.CardNumber AND Patient.PatientUsername=$s"
        c=db.cursor()
        c.execute(sql, (self.Username,))
        db.commit

        CardInfo=[]
        for item in c:
            CardInfo.append(item)
  
        self.root8.CardHolderName= listA[0][1]
        self.root8.CardNumber= listB[0][0]
        self.root8.CardType= listC[0][4]
        self.root8.CardCVV= listD[0][2]
        self.root8.CardDOE= listE[0][3]

        c.close()
        db.close()

        self.root8.e1.insert(0, self.root8.CardHolderName)
        self.root8.e2.insert(0, self.root8.CardNumber)
        self.root8.var1= self.root8.CardType
        self.root8.e3.insert(0, self.root8.CardCVV)
        self.root8.e4.insert(0, self.root8.CardDOE)
            
    def AddToBasket(self):
    
        db= self.Connect()
        createdSQL = "SELECT Visit.VisitID, DocUsername, PatientUsername, MedicineName FROM Visit, Prescription WHERE Visit.VisitID = Prescription.VisitID AND PatientUsername =$s" 
        c=db.cursor()
        c.execute(createdSQL, (self.Username,)) #second argument is a tuple, even if it is one element
        db.commit

        c.close()
        db.close()
        
        for item in createdSQL:
            self.listVerification.append(item)
        #VisitID, DocUsername, PatientUsername, MedicineName

        if len(listVerification)>0:
            self.medicationList.append(self.root7.e1.get())
            self.medicationList.append(self.root7.var1.get())
            self.medicationList.append(self.root7.var2.get())
            self.medicationList.append(self.root7.var3.get()) 
            self.medicationList.append(self.root7.e2.get())
            self.medicationList.append(self.root7.e3.get())
    

        else:
            messagebox.showerror("Invalid Error", "Your entry des not match with you prescription")
            
    def orderComfirmation(self):
        self.root50=Toplevel()
        self.root50.title('How Would You Like to Proceed?')

        self.root50.l1= Label(self.root8, text= self.medicationList[0])
        self.root50.l1.grid(row=0, column=0, sticky=W)

        self.root50.b1= Button(self.root50, text="Add More Medication", command=self.OrderMedication)
        self.root50.b1.grid(row=1, column=0, sticky=E)

        self.root50.b2= Button(self.root50, text="Checkout", command=self.PaymentInformation)
        self.root50.b2.grid(row=1, column=1, sticky=E)

    def OrderMeds(self):
        self.root8.withdraw()
        print(self.listVerification)

        db= self.Connect()
        sql= "UPDATE Prescription SET Ordered = 'Yes' WHERE Prescription.VisitID =%s AND Prescription.MedicineName = %s"
        c=db.cursor()
        c.execute(sql,  (self.listVerification[0][0], self.listVerification[0][3]))
        db.commit

        c.close()
        db.commit()
        self.PatientHomepage()
        

    def VisitHistory(self):
        #self.rootx.destroy()
        self.root9=Toplevel()
        self.root9.title('View Visit History')

        f1= Frame(self.root9)
        f1.pack()

        self.root9.l1= Label(f1, text="Dates of Visit")
        self.root9.l1.pack()

        db= self.Connect()
        sql= "SELECT Visit.DOV FROM Visit WHERE PatientUsername=%s"
        c=db.cursor()
        c.execute(sql, (self.Username,))
        db.commit

        Visits=[]
        for item in c:
            Visits.append(item)
        print(Visits)
    
        c.close()
        db.close()

        NumVisits= len(Visits)        

        for i in list(range(0,NumVisits)):
            vtext= Visits[i]
            print(vtext[0])
            
            self.root9.e= Button(f1, text= vtext[0], command=self.VisitHistory2(vtext[0]))
            self.root9.e.pack()

    def VisitHistory2(self,DOV):
        f2= Frame(self.root9)
        f2.pack()



        db= self.Connect()
        sql= "SELECT Visit.VisitID, FName, LName, DiastolicPressure, SystolicPressure FROM Visit, Doctor WHERE PatientUsername=%s AND DOV=%s AND Visit.DocUsername=Doctor.DocUsername"
        c=db.cursor()
        c.execute(sql, (self.Username,DOV))
        db.commit

        Info=[]
        for item in c:
            Info.append(item)

        print(Info)

        sql= "SELECT Diagnosis FROM Visit_Diagnosis WHERE VisitID=%s"
        c=db.cursor()
        c.execute(sql, (Info[0][0],))
        db.commit

        Info1=[]
        for item in c:
            Info1.append(item)

        print(Info1)

        sql= "SELECT MedicineName, Dosage, Duration, Notes FROM Prescription WHERE VisitID=%s"
        c=db.cursor()
        c.execute(sql, (Info[0][0],))
        db.commit

        Info2=[]
        for item in c:
            Info2.append(item)

        print(Info2)
        
        c.close()
        db.close()

        self.root9.l1= Label(f2, text='Consulting Doctor')
        self.root9.l1.grid(row=0, column=0)

        self.root9.e1=Entry(f2, width=60)
        self.root9.e1.grid(row=0, column=1)
        self.root9.e1.insert(0, Info[0][1]+Info[0][2])

        self.root9.l2= Label(f2, text='Blood Pressure:')
        self.root9.l2.grid(row=1, column=0)

        self.root9.l2= Label(f2, text='Systolic:')
        self.root9.l2.grid(row=1, column=1)

        self.root9.e3=Entry(f2, width=60)
        self.root9.e3.grid(row=1, column=2)
        self.root9.e3.insert(0, Info[0][4])

        self.root9.l4= Label(f2, text='Diastolic:')
        self.root9.l4.grid(row=1, column=3)

        self.root9.e4=Entry(f2, width=60)
        self.root9.e4.grid(row=1, column=4)
        self.root9.e4.insert(0, Info[0][3])

        self.root9.l5= Label(f2, text='Diagnosis')
        self.root9.l5.grid(row=2, column=0)

        self.root9.e5=Entry(f2, width=60)
        self.root9.e5.grid(row=2, column=1)
        #self.root9.e5.insert(0, Info1[0])

        ##########
        af= Frame(self.root9)
        af.pack()

        group= LabelFrame(af, text='Medications Prescribed: ', padx=5, pady=5)
        group.pack(padx=10, pady=10)
        
        self.root9.l7= Label(group, text='Medicine Name')
        self.root9.l7.pack()

        self.root9.l8= Label(group, text='Dosage')
        self.root9.l8.pack()

        self.root9.l9= Label(group, text='Duration')
        self.root9.l9.pack()

        self.root9.l10= Label(group, text='Notes')
        self.root9.l10.pack()

        f3=Frame(self.root9)

        for i in list(range(1,len(Info2))):#change everything depending on sql returns
            for j in list(range(0,4)):
                vtext= Info[i][j] #definitely need to change this!
                self.root9.l= Label(f3, text=vtext, relief= RIDGE)
                self.root9.l.grid(row= i, column=j)

    def RateDoctor(self):
        self.root5.withdraw()
        self.root10= Toplevel()
        self.root10.title("Rate A Doctor")

        db= self.Connect()
        sql= "SELECT Visit.DocUsername, FName, LName FROM Doctor, Visit WHERE Visit.DocUsername=Doctor.DocUsername AND Visit.PatientUsername=%s"
        c=db.cursor()
        c.execute(sql,(self.Username,))
        db.commit

        self.DoctorsInfo=[]
        self.DoctorsVisited=[]
        for item in c:
            self.DoctorsInfo.append(item)
            self.DoctorsVisited.append(item[1]+ ' ' +item[2])
        print(self.DoctorsInfo)
        print('hi')
        print(self.DoctorsVisited)
        
        c.close()
        db.close()

        self.root10.l1= Label(self.root10, text='Select Doctors: ')
        self.root10.l1.grid(row=1, column=0)

        self.root10.var1 = tkinter.StringVar(self.root10)
        self.root10.var1.set('')
        choices1 = self.DoctorsVisited
        self.root10.option1 = tkinter.OptionMenu(self.root10, self.root10.var1, *choices1)
        self.root10.option1.grid(row=1, column=1)

        self.root10.l2= Label(self.root10, text='Rating: (min=0, max=5)')
        self.root10.l2.grid(row=2, column=0)

        self.root10.var2 = tkinter.StringVar(self.root10)
        self.root10.var2.set('0')
        choices2 = ['0','1','2','3','4','5']
        self.root10.option2 = tkinter.OptionMenu(self.root10, self.root10.var2, *choices2)
        self.root10.option2.grid(row=2, column=1)

        self.root10.b1= Button(self.root10, text='Submit Rating', command=self.SubmitRating)
        self.root10.b1.grid(row=3, column=0)

    def SubmitRating(self):
        self.root10.withdraw()
        #self.rootx (open another window)

        for i in self.DoctorsVisited:
            A= i
            if A==self.root10.var1.get():
                self.DU= i[0]

        db= self.Connect()
        sql= "SELECT Rating From Doctor_Rating as d WHERE d.DocUsername=%s AND d.PatientUsername = %s"
        c=db.cursor()
        c.execute(sql, ( self.DU, self.Username) )
        db.commit

        B=[]
        for item in c:
            B.append(item)
        Blen=len(B)

        if Blen==0:
            db= self.Connect()
            sql= "INSERT INTO Doctor_Rating(`DocUsername`,`PatientUsername`,`Rating`) VALUES (%s,%s,%s) "
            c=db.cursor()
            c.execute(sql, ( self.DU, self.Username, self.root10.var2.get()) )
            db.commit
        else:
            db= self.Connect()
            sql= " UPDATE Doctor_Rating SET Rating = %s WHERE DocUsername = %s AND PatientUsername = %s"
            c=db.cursor()
            c.execute(sql, ( self.root10.var2.get(), self.DU, self.Username ))
            db.commit            
        
        c.close()
        db.close()
        self.PatientHomepage()

    
    def EditProfile(self):
        pass

    
    def NumberofMsgs(self):
        pass
        

###############################################################################################

##################################################################################

    def appointmentsCalendar(self):
        self.root34= Toplevel()
        self.root34.title("Appointments Calendar")

        if month == "January" or "March" or "May" or "August" or "July" or "October" or "December":
            count = 1
            newCount = 7
            counter = 0
            statement = True
            while statement == True:
                count = count + 1
                for y in range(newCount):
                    counter = counter + 1
                    self.root34.l1= Label(self.root34, text= str(counter, paitentCount), width= 10, state=DISABLED)
                    self.root34.l1.grid(row = count, column = y, sticky = E)
                    relief = RIDGE
                    if counter >= 31:
                        statement = False
                        break
                    else:
                        print("max reached")

        if month == "April" or "June" or "September" or "November":
            count = 1
            newCount = 7
            counter = 0
            statement = True
            while statement == True:
                count = count + 1
                for y in range(newCount):
                    counter = counter + 1
                    self.root34.l1= Label(self.root34, text= str(counter, paitentCount), width= 10, state=DISABLED)
                    self.root34.l1.grid(row = count, column = y, sticky = E)
                    relief = RIDGE
                    if counter >= 30:
                        statement = False
                        break
                    else:
                        print("max reached")

        if month == "February":
            count = 1
            newCount = 7
            counter = 0
            statment = True
            while statement == True:
                count = count + 1
                for y in range(newCount):
                    counter = counter + 1
                    self.root34.l1= Label(self.root34, text= str(counter, paitentCount), width= 10, state=DISABLED)
                    self.root34.l1.grid(row = count, column = y, sticky = E)
                    relief = RIDGE
                    if counter >= 28:
                        statement = False
                        break
                    else:
                        print("max reached")

        else:
            messagebox.showerror("Invalid Error", "Month Entered is Invalid")

    def DoctorHomepage(self):
        self.root15=Toplevel()
        self.root15.title('Homepage for Doctors')

        self.root15.b1= Button(self.root5, text="View Appointments Calendar", command=self.SearchAppointmentPage)
        self.root15.b1.pack()
        self.root15.b2= Button(self.root5, text="PatientVisits", command=self.VisitHistory)
        self.root15.b2.pack()
        self.root15.b3= Button(self.root5, text="Record a Surgery", command=self.OrderMeds)
        self.root15.b3.pack()
        self.root15.b4= Button(self.root5, text="Communicate", command=self.Communicate)
        self.root15.b4.pack()
        self.root15.b5= Button(self.root5, text="Edit Profile", command=self.RateDoctor)
        self.root15.b5.pack()
        ##self.root15.e1= Entry(self.root5, text="Edit Profile", command=self.RateDoctor)
        ##self.root15.e1.pack()

        
#######################Kevin's Code###############################
            
    def patVisitHistory(self):
        #self.rootx.destroy()
        self.root89=Toplevel()
        self.root89.title('Patient Visit History')
        
        
        self.sv1 = StringVar()
        self.sv2 = StringVar()
        
        self.recVisitrVL1 = Label(self.root89, text ="Name:", pady = 3)
        self.recVisitrVL1.grid(row = 0, column = 0)

        self.recVisitrVE1 = Entry(self.root89, textvariable = self.sv1, width = 30, state = NORMAL)
        self.recVisitrVE1.grid(row = 0, column = 1)

        self.recVisitrVL2 = Label(self.root89, text ="Phone:", pady = 3)
        self.recVisitrVL2.grid(row = 0, column = 2)

        self.recVisitrVE2 = Entry(self.root89, textvariable = self.sv2, width = 30, state = NORMAL)
        self.recVisitrVE2.grid(row = 0, column = 3)

        self.recVisitrVB1 = Button(self.root89, text = "Search", command = self.Connect)
        self.recVisitrVB1.grid(row = 0, column = 4)

        self.recVisitrVL2 = Label(self.root89, text ="Patient Name:", pady = 3)
        self.recVisitrVL2.grid(row = 1, column = 0)

        self.recVisitrVL3 = Label(self.root89, text ="Phone Number:", pady = 3)
        self.recVisitrVL3.grid(row = 1, column = 1)

        self.recVisitrVB2 = Button(self.root89, text = "View", command = self.patientResults)
        self.recVisitrVB2.grid(row = 1, column = 2)

        self.recVisitrVB3 = Button(self.root89, text = "Record a visit", command = self.recordVisit)
        self.recVisitrVB3.grid(row = 1, column = 3)

        self.patNameList = Listbox(self.root89, width = 20, selectmode = BROWSE)
        self.patNameList.grid(row = 2, column = 0)

        self.patNumList = Listbox(self.root89, width = 20, height = 10, selectmode = BROWSE)
        self.patNumList.grid(row = 2, column = 1)

        self.recVisitrVL4 = Label(self.root89, text ="Dates of Visits", pady = 3)
        self.recVisitrVL4.grid(row = 3, column = 0)

        self.dOvList = Listbox(self.root89, width = 20, selectmode = BROWSE)
        self.dOvList.grid(row = 4, column = 0)

        #self.DOV = self.dOvList.get(self.dOvList.curselection())
        self.DOV = StringVar()
        self.sys = StringVar()
        self.dias = StringVar()
        #create the self.dOvList by appending the values of the dates....

        self.aFrame = Frame(self.root89, width = 100, height = 100, borderwidth = 1)
        self.aFrame.grid(row = 4, column = 1)

        self.recVisitrVL5 = Label(self.aFrame, text ="Date of Visit:", pady = 3)
        self.recVisitrVL5.grid(row = 0, column = 0)

        self.recVisitrVE3 = Entry(self.aFrame, textvariable = self.DOV, width = 20, state = NORMAL)
        self.recVisitrVE3.grid(row = 0, column = 1)

        self.recVisitrVL6 = Label(self.aFrame, text ="Blood Pressure:", pady = 3)
        self.recVisitrVL6.grid(row = 1, column = 0)

        self.recVisitrVL9 = Label(self.aFrame, text ="Systolic:", pady = 3)
        self.recVisitrVL9.grid(row = 1, column = 1)

        self.recVisitrVE4 = Entry(self.aFrame, textvariable = self.sys  , width = 10, state = NORMAL)
        self.recVisitrVE4.grid(row = 1, column = 2)

        self.recVisitrVL10 = Label(self.aFrame, text ="Diastolic:", pady = 3)
        self.recVisitrVL10.grid(row = 1, column = 3)

        self.recVisitrVE5 = Entry(self.aFrame, textvariable = self.dias  , width = 10, state = NORMAL)
        self.recVisitrVE5.grid(row = 1, column = 4)

        self.recVisitrVL7 = Label(self.aFrame, text ="Diagnosis:", pady = 3)
        self.recVisitrVL7.grid(row = 3, column = 0)

        ############make the textbox for diagnosis during visit#########
        self.sFrame = Frame(self.aFrame,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken") ### check
        scrollbar = tkinter.Scrollbar(self.sFrame) 
        self.editArea4 = tkinter.Text(self.sFrame, width=30, height=5, wrap="word",
                               yscrollcommand=scrollbar.set,
                               borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea4.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea4.pack(side="left", fill="both", expand=True)
        self.sFrame.grid(row = 3, column = 1)

        #print(self.editArea4.get(1.0, tkinter.END)) #gets the string from the textbox
        #self.editArea4.delete(1.0, tkinter.END) # deletes the entry in the textbox


        #self.editArea4.insert(INSERT, self.editArea2.get(1.0, tkinter.END))
        
        self.recVisitrVL8 = Label(self.aFrame, text ="Medications Prescribed:", pady = 3)
        self.recVisitrVL8.grid(row = 5, column = 0)

        self.recVisitrVL9 = Label(self.aFrame, text ="Medicine Name:", pady = 3)
        self.recVisitrVL9.grid(row = 4, column = 1)

        self.recVisitrVL10 = Label(self.aFrame, text = "Dosage:", pady = 3)
        self.recVisitrVL10.grid(row = 4, column = 2)

        self.recVisitrVL11 = Label(self.aFrame, text ="Duration:", pady = 3)
        self.recVisitrVL11.grid(row = 4, column = 3)

        self.recVisitrVL12 = Label(self.aFrame, text ="Notes:", pady = 3)
        self.recVisitrVL12.grid(row = 4, column = 4)

    def patientResults(self):
        #self.selectedValue = self.patNamNumList.get(self.patNamNumList.curselection())
        self.selectedValue = [["Vicodin", "5", "3 Days", "Fuck You"], ["Tylenol", "4", "20 Days"]]
        selectedValue = self.selectedValue
        i = 0
        self.selectItem = StringVar()
        for item in range(len(selectedValue)):

            print(selectedValue[item][0])
            print(selectedValue[item][1])
            print(selectedValue[item][2])
            #print(selectedValue[item][3])
            
            self.recVisitrVE6 = Entry(self.aFrame)
            self.recVisitrVE6.insert(0, selectedValue[item][0])
            self.recVisitrVE6.grid(row = 5+i, column = 1)

            self.recVisitrVE7 = Entry(self.aFrame)
            self.recVisitrVE7.insert(0, selectedValue[item][1])
            self.recVisitrVE7.grid(row = 5+i, column =2 )

            self.recVisitrVE8 = Entry(self.aFrame)
            self.recVisitrVE8.insert(0, selectedValue[item][2])
            self.recVisitrVE8.grid(row = 5+i, column = 3)

            try:
                self.recVisitrVE9 = Entry(self.aFrame)
                self.recVisitrVE9.insert(0, selectedValue[item][3])
                self.recVisitrVE9.grid(row = 5+i, column = 4)

            except:
                self.recVisitrVE9 = Entry(self.aFrame)
                self.recVisitrVE9.insert(0, " ")
                self.recVisitrVE9.grid(row = 5+i, column = 4)

            i += 1

    def recordVisit(self):
        self.root89.withdraw()
        self.recVisit = Toplevel()
        self.recVisit.title("Record Visit")

        

        self.rV1 = StringVar()
        self.rV2 = StringVar()
        self.rV3 = StringVar()
        self.rV4 = StringVar()
        self.rV5 = StringVar()

        self.sysBPList = []
        self.diaBPList = []
        self.diagnosisList = []
        self.drugList = []
        self.dosageList = []
        self.durationList = []
        self.notesList = []
        self.count = 0

        now = datetime.today()
        a = str(now)

        rVL1 = Label(self.recVisit, text ="Date of Visit:", pady = 3)
        rVL1.grid(row = 0, column = 0)

        rVE1 = Label(self.recVisit, text = a, pady = 3)
        rVE1.grid(row = 0, column = 1)

        rVL2 = Label(self.recVisit, text ="Patient Name:", pady = 3)
        rVL2.grid(row = 1, column = 0)

        rVE2 = Entry(self.recVisit, textvariable = self.sv1.get(), width = 30, state = 'readonly')
        rVE2.grid(row = 1, column = 1)

        rVL3 = Label(self.recVisit, text ="Blood Pressure:", pady = 3)
        rVL3.grid(row = 2, column = 0)

        rVL5 = Label(self.recVisit, text ="Systolic:", pady = 3)
        rVL5.grid(row = 2, column = 1)

        rVE3 = Entry(self.recVisit, textvariable = self.rV3, width = 10, state = NORMAL)
        rVE3.grid(row = 2, column = 2)

        rVL6 = Label(self.recVisit, text ="Diastolic:", pady = 3)
        rVL6.grid(row = 2, column = 3)

        rVE4 = Entry(self.recVisit, textvariable = self.rV4, width = 10, state = NORMAL)
        rVE4.grid(row = 2, column = 4)

        rVL4 = Label(self.recVisit, text ="Diagnosis:", pady = 3)
        rVL4.grid(row = 3, column = 0)

        ###########make the textbox for diagnosis during visit#########
        sFrame = Frame(self.recVisit,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(sFrame) 
        self.editArea2 = tkinter.Text(sFrame, width=30, height=5, wrap="word",
                               yscrollcommand=scrollbar.set,
                               borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea2.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea2.pack(side="left", fill="both", expand=True)
        sFrame.grid(row = 3, column = 1)

        #print(self.editArea2.get(1.0, tkinter.END)) #gets the string from the textbox
        #self.editArea2.delete(1.0, tkinter.END) # deletes the entry in the textbox

        #rVB1 = Button(self.win, text = "Back", command = self.PatientHomepage)
        #rVB1.grid(row = 7, column = 7)

        
        ############################### bottom half of Record Visit GUI#############################

        self.recVFrame = Frame(self.recVisit, width = 100, height = 100, borderwidth = 1)
        self.recVFrame.grid(row = 4, column = 0)
        rVL7 = Label(self.recVFrame, text ="Prescribe Medication", pady = 10)
        rVL7.grid(row = 1, column = 1, columnspan = 5)

        rVL8 = Label(self.recVFrame, text ="Drug Name:")
        rVL8.grid(row = 2, column = 0)

        rVE5 = Entry(self.recVFrame, textvariable = self.rV5, width = 30, state = NORMAL)
        rVE5.grid(row = 2, column = 1)

        ################ dosage ###################
        rVL9 = Label(self.recVFrame, text ="Dosage:")
        rVL9.grid(row = 3, column = 0)

        var1 = tkinter.StringVar(self.root89)
        var1.set('1')
        choices = ['1','2','3', '4', '5', '6', '7', '8', '9', '10']
        self.recVFrame.option = tkinter.OptionMenu(self.recVFrame, var1, *choices)
        self.recVFrame.option.grid(row=3, column=1)

        rVL12 = Label(self.recVFrame, text ="per day")
        rVL12.grid(row = 3, column = 2)
                        
        self.recVFrame.doseChose= var1.get() #value of drop down dosage type

        ###################### duration ###################
        rVL10 = Label(self.recVFrame, text ="Duration:")
        rVL10.grid(row = 4, column = 0)

        var2 = tkinter.StringVar(self.root89)
        var2.set('0')
        choices = ['0', '1','2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.recVFrame.option = tkinter.OptionMenu(self.recVFrame, var2, *choices)

        self.recVFrame.option.grid(row=4, column= 1)

        rVL13 = Label(self.recVFrame, text ="months")
        rVL13.grid(row = 4, column = 2)
                        
        self.recVFrame.monthChose= var2.get() #value of drop down month type

        var3 = tkinter.StringVar(self.root89)
        var3.set('0')
        choices = ['0','1','2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.recVFrame.option = tkinter.OptionMenu(self.recVFrame, var3, *choices)

        self.recVFrame.option.grid(row= 4, column=3)

        rVL13 = Label(self.recVFrame, text ="days")
        rVL13.grid(row = 4, column = 4)
                        
        self.recVFrame.dayChose= var3.get() #value of drop down day type


        ######################## notes #########################################3
        rVL11 = Label(self.recVFrame, text ="Notes:")
        rVL11.grid(row = 5, column = 0)

        sFrame2 = Frame(self.recVFrame,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(sFrame2) 
        self.editArea3 = tkinter.Text(sFrame2, width=30, height=5, wrap="word",
                               yscrollcommand=scrollbar.set,
                               borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea3.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea3.pack(side="left", fill="both", expand=True)
        sFrame2.grid(row = 5, column = 1)

        #print(self.editArea3.get(1.0, tkinter.END)) #gets the string from the textbox
        #self.editArea3.delete(1.0, tkinter.END) # deletes the entry in the textbox

        self.rVB1 = Button(self.recVisit, text = 'Submit', command = self.Connect)
        self.rVB1.grid(row = 10, column = 7)

        self.rVB2 = Button(self.recVisit, text = 'Add New Prescription', command = self.addMed)
        self.rVB2.grid(row = 10, column = 6)

        #scrollbar = Scrollbar(self.win)
        #scrollbar.pack( side = RIGHT, fill=Y )

        #mylist = Listbox(self.win, yscrollcommand = scrollbar.set )
        #for line in range(100):
           #mylist.insert(END, "This is line number " + str(line))

        #mylist.pack( side = LEFT, fill = BOTH )
        #scrollbar.config( command= self.recVFrame.yview )

    def addMed(self):

        self.sysBPList.append([self.rV3])
        self.diaBPList.append([self.rV4])
        self.diagnosisList.append([self.editArea2.get(1.0, tkinter.END)])
        self.drugList.append([self.rV5])
        self.dosageList.append([self.recVFrame.doseChose])
        self.durationList.append([self.recVFrame.monthChose, self.recVFrame.dayChose])
        self.notesList.append([self.editArea3.get(1.0, tkinter.END)])
        
        self.count += 1
        i = self.count
        j = self.count + 5

        ### add another frame to add prescription pane ####
        frame = Frame(self.recVisit, width = 100, height = 100, borderwidth = 1)
        frame.grid(row = 4+i, column = 0)
        rVL7 = Label(frame, text ="Prescribe Medication", pady = 10)
        rVL7.grid(row = 1, column = 1, columnspan = 5)

        rVL8 = Label(frame, text ="Drug Name:")
        rVL8.grid(row = 2, column = 0)

        rVE5 = Entry(frame, textvariable = self.rV5, width = 30, state = NORMAL)
        rVE5.grid(row = 2, column = 1)

        ################ dosage ###################
        rVL9 = Label(frame, text ="Dosage:")
        rVL9.grid(row = 3, column = 0)

        var1 = tkinter.StringVar(self.root89)
        var1.set('1')
        choices = ['1','2','3', '4', '5', '6', '7', '8', '9', '10']
        frame.option = tkinter.OptionMenu(frame, var1, *choices)
        frame.option.grid(row=3, column=1)

        rVL12 = Label(frame, text ="per day")
        rVL12.grid(row = 3, column = 2)
                        
        self.recVFrame.doseChose= var1.get() #value of drop down dosage type

        ###################### duration ###################
        rVL10 = Label(frame, text ="Duration:")
        rVL10.grid(row = 4, column = 0)

        var2 = tkinter.StringVar(self.recVisit)
        var2.set('1')
        choices = ['1','2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        frame.option = tkinter.OptionMenu(frame, var2, *choices)

        frame.option.grid(row=4, column= 1)

        rVL13 = Label(frame, text ="months")
        rVL13.grid(row = 4, column = 2)
                        
        self.recVFrame.monthChose= var2.get() #value of drop down month type

        var3 = tkinter.StringVar(self.recVisit)
        var3.set('1')
        choices = ['1','2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        frame.option = tkinter.OptionMenu(frame, var3, *choices)

        frame.option.grid(row= 4, column=3)

        rVL13 = Label(frame, text ="days")
        rVL13.grid(row = 4, column = 4)
                        
        self.recVFrame.dayChose= var3.get() #value of drop down day type


        ######################## notes #########################################3
        rVL11 = Label(self.recVFrame, text ="Notes:")
        rVL11.grid(row = 5, column = 0)

        sFrame2 = Frame(frame,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(sFrame2) 
        self.editArea3 = tkinter.Text(sFrame2, width=30, height=5, wrap="word",
                               yscrollcommand=scrollbar.set,
                               borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea3.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea3.pack(side="left", fill="both", expand=True)
        sFrame2.grid(row = 5, column = 1)

        #print(self.editArea3.get(1.0, tkinter.END)) #gets the string from the textbox
        #self.editArea3.delete(1.0, tkinter.END) # deletes the entry in the textbox

        # move the 'Submit' and "Add New Prescription' buttons down everytime new prescriptions are added
        self.rVB1.destroy()
        self.rVB2.destroy()
        self.rVB1 = Button(self.recVisit, text = 'Submit')
        self.rVB1.grid(row = 10+i, column = 7)

        self.rVB2 = Button(self.recVisit, text = 'Add New Prescription', command = self.addMed)
        self.rVB2.grid(row = 10+i, column = 6)

    def messages(self): ####need to find where this comes from####
        #self.root5.destroy() 
        self.messageUI = Toplevel()
        self.messageUI.title("Messages")
        
        msgL1 = Label(self.messageUI, text ="Status", pady = 3, padx = 3)
        msgL1.grid(row = 0, column = 0)

        msgL2 = Label(self.messageUI, text ="Date", pady = 3, padx = 3)
        msgL2.grid(row = 0, column = 1)

        msgL3 = Label(self.messageUI, text ="From", pady = 3, padx = 3)
        msgL3.grid(row = 0, column = 3)

        msgL4 = Label(self.messageUI, text ="Message", pady = 3, padx = 3)
        msgL4.grid(row = 0, column = 4)

        msgB1 = Button(self.messageUI, text = "Back", command = self.LoginScreen)
        msgB1.grid(row = 7, column = 7)

    def LoginScreen(self):
        pass
    
    def msgUIdoctor(self): # where does this come from####
        #self.rootx.destroy() 
        self.msgDocUI = Toplevel()
        self.msgDocUI.title("Send Message to Patients/Doctors")

        self.docMessage = StringVar()
        self.patMessage = StringVar()

        msgUIL1 = Label(self.msgDocUI, text ="Select Doctor:")
        msgUIL1.grid(row = 0, column = 0, pady = 4)

        msgUIL2 = Label(self.msgDocUI, text ="Select Patient:")
        msgUIL2.grid(row = 0, column = 4, pady = 4)

        msgUIL3 = Label(self.msgDocUI, text ="Message:")
        msgUIL3.grid(row = 3, column = 0, pady = 4)

        msgUIL4 = Label(self.msgDocUI, text ="Message:")
        msgUIL4.grid(row = 3, column = 4, pady = 4)


        #############################drop down menus to select patient and doctor###############
        
        self.docList = Listbox(self.msgDocUI, selectmode = BROWSE)
        self.docList.grid(row = 0, column = 1)
        #aList = range(100)

        #for i in aList:
            #self.docList.insert(i, i) #use this method to append doctor names to list


        self.patList = Listbox(self.msgDocUI, selectmode = BROWSE)
        self.patList.grid(row = 0, column = 5)
        
        self.getPatsandDocs()

        ############################### message boxes ###################################

        frame1 = Frame(self.msgDocUI,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(frame1) 
        self.docMessage = tkinter.Text(frame1, width=10, height=10, wrap="word",
                           yscrollcommand=scrollbar.set,
                           borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.docMessage.yview)
        scrollbar.pack(side="right", fill="y")
        self.docMessage.pack(side="left", fill="both", expand=True)
        frame1.grid(row = 4, column = 0)

        msgUIB2 = Button(self.msgDocUI, text = "Send Message", command = self.writeMsg2DB)
        msgUIB2.grid(row = 6, column = 6)

        frame2 = Frame(self.msgDocUI,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(frame2) 
        self.patMessage = tkinter.Text(frame2, width=10, height=10, wrap="word",
                           yscrollcommand=scrollbar.set,
                           borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.patMessage.yview)
        scrollbar.pack(side="right", fill="y")
        self.patMessage.pack(side="left", fill="both", expand=True)
        frame2.grid(row = 4, column = 4)

    def getPatsandDocs(self):
        #write SQL code here and append names of doctors and patients to listboxes


        aList = range(100)

        for i in aList:
            self.docList.insert(i, i) #use this method to append doctor names to list
        
    def writeMsg2DB(self):
        db = self.Connect()

        sql ="INSERT INTO SendsmesageToDoc(DocUsername, PatientUsername, DateTime, Content) VALUES (%s, %s, %s, %s );"
        c = db.cursor()
        
        #print(self.patientName.get())

        
        a = self.msgUIE1.get(1.0, tkinter.END) #gets the string from the textbox
        c.execute(sql, (a,)) #patient name created not right
        db.commit
        aList = []

    def msgUIpatient(self):
        #self.rootx.destroy() 
        self.msgDocUI = Toplevel()
        self.msgDocUI.title("Send Message to Doctor")
        
        self.patMessagefromPat = StringVar()

        msgUIL5 = Label(self.msgDocUI, text ="Select Name:")
        msgUIL5.grid(row = 0, column = 0, pady = 4)

        msgUIL7 = Label(self.msgDocUI, text ="Message:")
        msgUIL7.grid(row = 3, column = 0, pady = 4)

        sFrame = Frame(self.msgDocUI,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(sFrame) 
        self.msgUIE1 = tkinter.Text(sFrame, width=30, height=5, wrap="word",
                               yscrollcommand=scrollbar.set,
                               borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.msgUIE1.yview)
        scrollbar.pack(side="right", fill="y")
        self.msgUIE1.pack(side="left", fill="both", expand=True)
        sFrame.grid(row = 4, column = 0)

        msgUIB2 = Button(self.msgDocUI, text = "Send Message", command = self.writeMsg2DB)
        msgUIB2.grid(row = 5, column = 3)

    def getNamNum(self):
        try:
            #write SQL code here to retreive names and numbers of patients from database!

            #print("Gotcha!")
            #print(self.patSearch.get())

            
            self.patNum = [["Dexter Morgan", "770-985-8869"], ["Dexter Morgan","404-313-4605"]]
            print(self.patNum[1][0])

            for i in range(len(self.patNum)):
                #print(i)
                #print(self.patNum[i][0])
                #self.patNamNumList.insert(i, self.patSearch.get())
                self.patNamNumList.insert(i, str(self.patSearch.get() + "     " + self.patNum[i][1]))
                #self.values.append(str(self.patSearch.get())self.patNum[i][1]))
            
            ##print(self.values[0])
       
            # these for loops iterate to make labels with patient numbers and names
            
             #gets the value of the listbox (serves as dropdown)


            selectVal = self.patNamNumList.curselection() #gets the selected value from the listbox

            print(self.patNamNumList.get(ACTIVE))

            a = self.patNamNumList.get(ACTIVE)
            print(type(a))

            index = self.patNamNumList.curselection()
            print(index)
            
            #print(type(i))
            #print(i)
            #print(self.patNum[1][0])
            #print(self.patNum[i][0])
            #self.selectedPatient = self.patNum[i][0]

            #print(self.selectedPatient)

            #if self.patientNamNumList.get(ACTIVE)
            

            aTuple = ()
            print(len(aTuple))
        except:
            print("Please enter a name to search")

    def createRecord(self):        
        print(self.var1.get())
        #print(self.editArea5.get())
        print(self.editArea5.get(1.0, END)) #gets the string from the textbox

        try:
            #print("recorded!")
            #a = self.patNamNumList.curselection()
            #print(a)
            #print(self.patNamNumList.curselection())
            #print(type(list(self.patNamNumList.curselection())[0])) # gives you the list index of the selected value in a string value
            #selectNumVal = int(list(self.patNamNumList.curselection())[0])
            #print(selectNumVal)

            #selectVal = self.values[selectNumVal]
            
            selectVal = self.patNamNumList.curselection()[0] #gets the selected value from the listbox

            print(self.patNamNumList.get(ACTIVE))
            #print(self.patNamNumList.curselection())
            index = self.patNamNumList.curselection() # this gets the index of what is selected

            i = index[0]
            i = int(i)
            
            #print(type(i))
            #print(i)
            #print(self.patNum[1][0])
            #print(self.patNum[i][0])
            #self.selectedPatient = self.patNum[i][0]

            #print(self.selectedPatient)
            
        except:
            print("Select a name")

    def surgeryRecord(self):
        #self.win.withdraw() 
        self.surgeryRec = Toplevel()
        self.surgeryRec.title("Surgery Record")

        self.patSearch = StringVar()

        self.surgeryRecl1 = Label(self.surgeryRec, text = "Search Patient:")
        self.surgeryRecl1.grid(row = 1, column = 0,  columnspan = 4)

        self.surgeryRece1 = Entry(self.surgeryRec, textvariable = self.patSearch, width = 30, state = NORMAL)
        self.surgeryRece1.grid(row = 1, column = 5)

        self.surgeryRecb1 = Button(self.surgeryRec, text = "Search", command = self.getNamNum)
        self.surgeryRecb1.grid(row = 1, column = 6)

        ######### frame to return patient name and number #####################
        self.surgeryFrame = Frame(self.surgeryRec, width = 80, height = 80, borderwidth = 1)
        self.surgeryFrame.grid(row = 2, column = 0)

        self.surgeryRecl2 = Label(self.surgeryFrame, text = "Patient Name             Phone number")
        self.surgeryRecl2.grid(row = 0, column = 0, sticky = W)

        
        #list box created from which doctor selects the correct patient
        self.patNamNumList = Listbox(self.surgeryFrame, width = 40, selectmode = ACTIVE)
        self.patNamNumList.grid(row = 1, column = 0)

        ############### left frame #######################################
        self.surgeonName = StringVar()
        self.cptCode = StringVar()
        
        self.sFrame1 = Frame(self.surgeryRec, width = 80, height = 80, borderwidth = 1)
        self.sFrame1.grid(row = 10, column = 0)

        self.sF1L1 = Label(self.sFrame1, text = "Patient Name:")
        self.sF1L1.grid(row = 0, column = 0)

        self.sF1L2 = Label(self.sFrame1, text = "Surgeon Name:")
        self.sF1L2.grid(row = 1, column = 0)

        self.sF1L3 = Label(self.sFrame1, text = "Procedure Name:")
        self.sF1L3.grid(row = 2, column = 0)

        self.sF1L4 = Label(self.sFrame1, text = "CPT Code:")
        self.sF1L4.grid(row = 3, column = 0)

        self.sF1L5 = Label(self.sFrame1, text = "Number of Assistants:")
        self.sF1L5.grid(row = 4, column = 0)

        self.sF1L6 = Label(self.sFrame1, text = "Pre-operative Medications:")
        self.sF1L6.grid(row = 5, column = 0)

        self.sF1E1 = Entry(self.sFrame1, textvariable = self.patNamNumList.get(ACTIVE), width = 30, state = NORMAL)
        self.sF1E1.grid(row = 0, column = 1)

        self.sF1E2 = Entry(self.sFrame1, textvariable = self.surgeonName)
        self.sF1E2.grid(row = 1, column = 1)

        self.var1 = StringVar()
        self.var1.set('Craniotomy')
        self.choices1 = ['Craniotomy','Nephrectomy','Bursectomy', 'Tonsillectomy', 'Abortion']
        self.sFrame1.option = tkinter.OptionMenu(self.sFrame1, self.var1, *self.choices1)
        self.sFrame1.option.grid(row=2, column=1)
                    
        self.var1.get() #value of drop down procedure type
        

        #sF1D1 = 
        #SF1D1.grid(row = 2, column = 1)        
        
        self.var3 = StringVar()
        self.var3.set(' ')
        self.choices2 = ['44567.1','56235.1','78827.1','87812.1', '98290.1']
        self.sFrame1.option = tkinter.OptionMenu(self.sFrame1, self.var3, *self.choices2)
        self.sFrame1.option.grid(row=3, column=1)
                    
        self.var3.get() #value of drop down procedure type
        

        

        self.var2 = StringVar()
        self.var2.set('0')
        self.choices3 = ['0','1','2','3', '4', '5', '6', '7', '8', '9', '10']
        self.sFrame1.option = tkinter.OptionMenu(self.sFrame1, self.var2, *self.choices1)
        self.sFrame1.option.grid(row=4, column=1)
                    
        self.var2.get() #value of drop down procedure type

        #sF1D2 =
        #SF1D2.grid(row = 4, column = 1)

    

        ######I need a list of the preoperative medications available#######

        sFrame4 = Frame(self.sFrame1,width=80, height=80,bg = '#ffffff',
                      borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(sFrame4) 
        self.editArea5 = tkinter.Text(sFrame4, width=10, height=10, wrap="word",
                           yscrollcommand=scrollbar.set,
                           borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea5.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea5.pack(side="left", fill="both", expand=True)
        sFrame4.grid(row = 5, column = 1)


        
        ############### right frame #######################################
        self.sFrame2 = Frame(self.surgeryRec, width = 80, height = 80, borderwidth = 1)
        self.sFrame2.grid(row = 10, column = 20)

        sF2L1 = Label(self.sFrame2, text = "Anesthesia Start Time:")
        sF2L1.grid(row = 0, column = 0)
        self.var4 = StringVar()
        self.var4.set('0')
        choices4 = ['0:00','3:00','6:00','9:00', '12:00', '15:00', '18:00', '21:00']
        self.sFrame2.option = tkinter.OptionMenu(self.sFrame2, self.var4, *choices4)
        self.sFrame2.option.grid(row=0, column=1)

        

        sF2L2 = Label(self.sFrame2, text = "Surgery Start Time:")
        sF2L2.grid(row = 1, column = 0)
        self.var5 = StringVar()
        self.var5.set('0')
        choices5 = ['0:15','3:15','6:15','9:15', '12:15', '15:15', '18:15', '21:15']
        self.sFrame2.option = tkinter.OptionMenu(self.sFrame2, self.var5, *choices5)
        self.sFrame2.option.grid(row=1, column=1)
        
        sF2L3 = Label(self.sFrame2, text = "Surgery Completion Time:")
        sF2L3.grid(row = 2, column = 0)
        self.var5 = StringVar()
        self.var5.set('0')
        choices5 = ['0:30','3:30','6:30','9:30', '12:30', '15:30', '18:30', '21:30']
        self.sFrame2.option = tkinter.OptionMenu(self.sFrame2, self.var5, *choices5)
        self.sFrame2.option.grid(row=2, column=1)

        sF2L4 = Label(self.sFrame2, text = "Description of Complcations during surgery:")
        sF2L4.grid(row = 3, column = 0)

        ###########make the textbox for complications during surgery#########
        sFrame3 = Frame(self.sFrame2,width=80, height=80,bg = '#ffffff',
                      borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(sFrame3) 
        self.editArea = tkinter.Text(sFrame3, width=10, height=10, wrap="word",
                           yscrollcommand=scrollbar.set,
                           borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea.pack(side="left", fill="both", expand=True)
        sFrame3.grid(row = 3, column = 1)

        b1 = Button(self.surgeryRec, text = "Record", command = self.createRecord)
        b1.grid(row = 20, column = 20)

        #print(self.editArea.get(1.0, tkinter.END)) #gets the string from the textbox
        #self.editArea.delete(1.0, tkinter.END) # deletes the entry in the textbox
        

        
    
        """
        #########text box creation code ##################
        
        frame1 = Frame(self.win,width=80, height=80,bg = '#ffffff',
                          borderwidth=1, relief="sunken")
        scrollbar = tkinter.Scrollbar(frame1) 
        self.editArea = tkinter.Text(frame1, width=10, height=10, wrap="word",
                           yscrollcommand=scrollbar.set,
                           borderwidth=0, highlightthickness=0)
        scrollbar.config(command=self.editArea.yview)
        scrollbar.pack(side="right", fill="y")
        self.editArea.pack(side="left", fill="both", expand=True)
        frame1.grid(row = 5, column = 6)

        msgUIB2 = Button(self.win, text = "Send Message", command = self.writeMsg2DB)
        msgUIB2.grid(row = 6, column = 6)
        
        #win.mainloop()



        
        
        container = Frame(master = self.surgeryRec)
        text = Text(container,
                    
        
        self.txt = tkst.ScrolledText(self.win, undo=True)
        self.txt['font'] = ('consolas', '12')
        self.txt.pack(expand=True, fill='both')
        """
            
rootWin=Tk()
Start= GTMRS(rootWin)
rootWin.mainloop()
