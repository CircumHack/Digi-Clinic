from datetime import date
import mysql.connector as mysql
import json
class DigiSQL:
    def __init__(self,host,user,password):
        self.con=mysql.connect(host=host,user=user,password=password)
        self.cur=self.con.cursor()
        self.cur.execute('''USE digi_clinic''')
        #AUTOMATED STATEMENT
    def track(self,data):
            ##### USED FOR HISTORY """"
        if self.new_patient_book:
            d=['Application for Medical Record was done and ']
        ins='''INSERT INTO activities(Date_and_Time,Activity,User_ID,Type) VALUES (NOW(),"%s","%s","%s")''' % (d[0],d[1],d[2])
        self.cur.execute(ins)
        self.con.commit()
    """   FOR ALL  """
    def get_date_text(self,date):
        d={'Sun':'Sunday','Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thu':'Thursday','Fri':'Friday','Sat':'Saturday'}
        m={'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July','Aug':'August','Sep':'September','Oct':'October','Nov':'November','Dec':'December'}
        newdate=date.ctime().replace('00:00:00','')
        for i in d:
            if i in newdate:
                newdate=newdate.replace(i,d[i])
                break
        for i in m:
            if i in newdate:
                newdate=newdate.replace(i,m[i])
                break
        return newdate
    """   FOR ALL  """
    def stop_collision_id(self,id,type):
        if type=='User':
            self.cur.execute('''SELECT ID FROM user WHERE ID="%s" '''%id)
            ids=sum(self.cur.fetchall(),())    
            if len(ids)>0:
                while True:
                    s=random.randrange(1000,9999)
                    self.cur.execute('''SELECT ID FROM user WHERE ID="%s" '''%id[:-4]+str(s))
                    ids=sum(self.cur.fetchall(),())
                    if len(ids)==0:
                        return id[:-4]+str(s)
            return id 
    """   FOR PATIENT  """       
    def book_new_user(self,data:dict,now):        
        # ID Generation
        id=self.stop_collision_id(data['ID'],'User')
        ### FIND AGE GRADE OF USER
        rem=date(now.year-18,now.month,now.day)-data['Real DOB']
        if rem.days<0:
            type='Child'
        else:
            rem=date(now.year-60,now.month,now.day)-data['Real DOB']
            if rem.days>-1:
                type='Elderly'
            else:
                type='Adult'
        ####  BOOKINGS CHECK
        if type!='Child':
            self.cur.execute('''SELECT Email FROM user WHERE Email="%s"'''%(data['Email']))
            emails=sum(self.cur.fetchall(),())
            if len(emails)>0:
                return 'Email has been used by an existing customer'
            self.cur.execute('''SELECT Phone_Number FROM user WHERE Phone_Number="%s"-'''%(data['Phone']))
            phones=sum(self.cur.fetchall(),())
            if len(phones)>0:
                return 'Phone Number has been used by an existing customer'
            self.cur.execute('''SELECT Identity_Number FROM user WHERE Identity_Number="%s"'''%(data['NIN']))
            idno=sum(self.cur.fetchall(),())
            if len(idno)>0:
                return 'Account Already exists'            
        self.cur.execute('''SELECT ID FROM user WHERE ID="%s"'''%data['NID'])
        nid=sum(self.cur.fetchall(),())
        if len(nid)!=1:
            return 'Next of Kin has not been registered'
        self.cur.execute('''SELECT Department FROM hospital WHERE ID="%s"''')
        dep=sum(self.cur.fetchall(),())[0]
        dep=json.loads(dep)
        depid=None
        for i in dep:
            if dep[i]==data['Reason']:
                depid=i
                break
        if depid==None:
            #SEARCH FOR ONE
            return 'The Hospital can not meet your request'
        self.cur.execute('''SELECT Daily_Capacity FROM department WHERE ID="%s"''')
        daily_cap=sum(self.cur.fetchall(),())[0]
        if daily_cap<1:
            self.cur.execute('''SELECT Days_Booked FROM department WHERE ID="%s"''')
            booked=json.loads(sum(self.cur.fetchall(),())[0])
            if data['Appointment_DateTime'] in booked:
                while True:
                    data['Appointment_DateTime']=data['Appointment_DateTime']+timedelta(days=1)
                    self.cur.execute('''SELECT Days_Booked FROM department WHERE ID="%s"''')
                    booked=json.loads(sum(self.cur.fetchall(),())[0])
                    if data['Appointment_DateTime'] not in booked:
                        break
                return f'Hospital has been booked for this day. The hospital is available on {self.get_date_text(data["Appointment_DateTime"])} for your appointment.'
        self.cur.execute('''INSERT INTO user(ID,Name,DOB,Home_Address,Marital_Status,Picture,Identity_Number,Email,Phone_Number,Next_of_Kin_ID,Password,Type) 
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',[data['ID'],data['Name'],data['Address'],data['Marital_Status'],data['Picture'],data['NIN'],data['Email'],data['Phone'],data['NID'],data['Password'],data['Type']])
        self.cur.execute('''INSERT INTO appointment(UserID,Hospital_ID,Date_of_Appointment,Department_ID)
                         VALUES(%s,%s,%s,%s)''',[data['ID'],data['Hospital'],data['Appointment_DateTime'],depid])
        return 'Done'
    """   FOR DOCTORS  """
    def register_patient(self,data):
        self.cur.execute('''SELECT UserID WHERE HospitalID="%s" AND DepartmentID="%s" AND TIMESTAMPDIFF(DAY,Date_of_Appointment,NOW())=0''',data['Hospital'],data['Department'])
        uid=sum(self.cur.fetchall(),())
        if data['UserID'] not in uid:
            return 'User is not booked for today'
        self.cur.execute('''UPDATE user SET Blood_Group="%s",Rh_Factor="%s",Blood_Genotype="%s",Height="%s",Weight="%s",Allergies="%s",Vaccinations="%s",Challenges_&_Disabillities="%s",Health_Insurance_ID="%s",Registered=1 WHERE ID="%s" '''%(data['BG'],data['Rh'],data['Genotype'],data['Height'],data['Weight'],data['Allergy'],data['Vaccine'],data['C&D'],data['Insurance_ID'],data['ID']))
        self.cur.execute('''INSERT INTO wallet(UserID,Account_Number,Account_Balance,Savings_Scheme) VALUES(%s,%s,%s,%s,%s)''',[data['ID'],data['Account_Number'],0,data['Scheme']])
        return 'Done'
    def book_appointment(self,data):
        self.cur.execute('''SELECT Daily_Capacity FROM hospital WHERE Daily_Capactiy>=1 AND ID="%s"'''%data['Hospital'])
        cap=sum(self.cur.fetchall(),())
        if len(cap)<1:
            return 'The specified Hospital has reached full capacity'
        self.cur.execute('''SELECT Daily_Capacity FROM department WHERE Daily_Capactiy>=1 AND ID="%s"'''%data['Department'])
        cap=sum(self.cur.fetchall(),())
        if len(cap)>1:
            self.cur.execute('''INSERT INTO appointment(UserID,Department_ID,Date_of_Appointment,Reason) VALUES (%s,%s,%s,%s,%s)'''%(data['ID'],data['Department'],data['Appointment_Date'],data['Reason']))
            return 'Done'
        return 'The specified Department has reached full capacity'
    def add_funds(self,data):
        if data['Status']:
            self.cur.execute('''SELECT UserID FROM wallet WHERE UserID="%s"'''%data['ID'])
            if len(sum(self.cur.fetchall(),()))==1:
                self.cur.execute('''UPDATE wallet SET Account_Balance+="%s" WHERE UserID="%s"'''%(data['Balance'],data['ID']))
                return 'Done'
        else:
            return 'Unauthorised Transaction'
    def login(self,email,password):
        self.cur.execute('''SELECT ID FROM user WHERE Email="%s" AND Password="%s"'''%(email,password))
        ans=sum(self.cur.fetchall(),())
        if len(ans)==1:
            return ans[0]
        return False
    def withdraw_funds(self,data):
        if data['Status']:
            if data['Status']:
                self.cur.execute('''SELECT UserID FROM wallet WHERE UserID="%s"'''%data['ID'])
            if len(sum(self.cur.fetchall(),()))==1:
                self.cur.execute('''UPDATE wallet SET Account_Balance-="%s" WHERE UserID="%s"'''%(data['Balance'],data['ID']))
                return 'Done'
        else:
            return 'Unauthorised Transaction'
    def get_all_hospital(self):
        #GEO COORDINATE CALC
        self.cur.execute('''SELECT ID,Name,Hospital_Code,Address,Geo_Location,Picture_URL FROM hospital WHERE Daily_Capacity>=1''')
        data=self.cur.fetchall()
        info=[]
        for i in data:
            info.append({'ID':i[0],'Name':i[1],'Hospital_Code':i[2],'Address':i[3],'Geo_Location':{},'Picture':i[5]})
        return info
    def verify_email_phone(self,data,code,type):
        # VERIFY EMAIL AND PHONE
        self.cur.execute('''SELECT Email_Phone FROM verifyemailphone WHERE Valid=1 AND Type="Email" AND Email_Phone="%s"'''%data['Email'])
        emails=sum(self.cur.fetchall(),())        
        self.cur.execute('''SELECT Email_Phone FROM verifyemailphone WHERE Valid=1 AND Type="Phone" AND Email_Phone="%s"'''%data['Phone'])
        phones=sum(self.cur.fetchall(),())
        if len(emails)>0:
            return 'Email Verification Link has already been sent'
        if len(phones)>0:
            return 'Phone Verification Code has already been sent'
        self.cur.execute('''SELECT Email_Phone FROM verifyemailphone WHERE Email_Phone="%s" '''%(data['Email']))
        a=sum(self.cur.fetchall(),())
        self.cur.execute('''SELECT Email_Phone FROM verifyemailphone WHERE Email_Phone="%s" '''%(data['Phone']))
        b=sum(self.cur.fetchall(),())
        if type=='Email':
            if len(a)>0:
                self.cur.execute('''UPDATE verifyemailphone SET DateTime=NOW(),Code="%s" AND Valid=1 WHERE Email_Phone="%s"'''%(code,data['Email']))
            else:
                self.cur.execute('''INSERT INTO verifyemailphone(Email_Phone,Code,Type) VALUES (%s,%s,%s)''',[data['Email'],code,'Email'])
        else:
            if len(b)>0:
                self.cur.execute('''UPDATE verifyemailphone SET DateTime=NOW(),Code="%s" AND Valid=1 WHERE Email_Phone="%s"'''%(code,data['Phone']))
            else:
                self.cur.execute('''INSERT INTO verifyemailphone(Email_Phone,Code,Type) VALUES (%s,%s,%s)''',[data['Phone'],code,'Phone'])
        return 'Done'
    def check_verify(self,code,field,type):
        self.cur.execute('''SELECT Code FROM verifyemailphone WHERE Email_Phone="%s" AND Code="%s" AND Type="%s"'''%(field,code,type))
        data=sum(self.cur.fetchall(),())
        if len(data)==1:
            self.cur.execute('''DELETE FROM verifyemailphone WHERE Email_Phone="%s" '''%(field))
            return True
        return False
    def close(self):
        self.con.close()