from kivymd.app import MDApp
#from kivy.config import Config
from kivy.factory import Factory
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivy.clock import Clock
from kivy.core.window import Window
from kivycupertino.uix.textfield import CupertinoTextField
from akivymd.uix.datepicker import AKMonthPicker,AKDatePicker
from kivymd.uix.picker import MDTimePicker
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from plyer import filechooser
import firebasetest
from apis import DigiClinicAPIS
from widget import MySnackBar,HospitalButtom,HospitalList,MyDialog,MainAlert
from digisql import DigiSQL
from digiemail import EmailSender
import datetime,os,check,random,encrypt
class DigiManager(ScreenManager):
    def __init__(self,**kwargs):
        super(DigiManager,self).__init__(**kwargs)
        self.email_verify=''
        self.phone_verify=''
        self.snackbar=MySnackBar(text='',icon='') 
        self.account_pic='pics/account.png'       
        self.snackbar.size_hint_x=(Window.width-(self.snackbar.snackbar_x*2.5))/Window.width
        self.dialog=MyDialog()
        self.dialog.background_color=app.theme_cls.primary_dark
        self.email=EmailSender()
    def show_remarks(self,text,color,icon='alert'):
        self.snackbar.text=text
        self.snackbar.icon=icon
        self.snackbar.md_bg_color=color
        self.snackbar.open()
    def back_screen(self,name):
        self.current=name
    def change_screen(self,name):
        if name=='create_ind_wallet':
            bvn=self.ids.ind_wallet.ids.bvn.text
            pin=self.ids.ind_wallet.ids.pin.text
            if bvn=='' and len(bvn)!=11:
                self.show_remarks('Invalid BVN',(1,0,0,1))
            elif pin=='':
                self.show_remarks('Invalid PIN',(1,0,0,1))
            else:
                res=app.digiapi.bvn_encrypt(bvn)
                if res:
                    res=app.digiapi.create_wallet('circumokosun@gmail.com')#self.data['Email'])
                    if res:
                        self.show_remarks('Wallet Created',(1,1,1,1),'information')
                        self.current='new_wallet'
                        self.ids.new_wallet.ids.icon_ind.icon='check'
                    #else:
                    #    self.show_remarks('Wallet Not Created',(1,0,0,1),'information')                        
                    self.current='new_wallet'
                    self.ids.new_wallet.ids.icon_ind.icon='check'
                else:
                    self.show_remarks('Invalid BVN',(1,1,1,1),'information')
        elif name=='create_ind_wallet':
            self.current='new_wallet'
            self.ids.new_wallet.ids.icon_ind.icon='check'
        elif name=='fam_wallet':
            self.ids.fam_wallet.ids.admin_rv.data=[{'admin':'OneLineIconListItem','text':'Add Administrator','picture':'plus','on_release':self.add_admin},{'admin':'PersonList','text':self.ids.personal.ids.fname.text+self.ids.personal.ids.lname.text+self.ids.personal.ids.oname.text,'picture':self.ids.picture.ids.image.source}]
            self.ids.fam_wallet.ids.member_rv.data=[{'member':'OneLineIconListItem','text':'Add Member','picture':'plus','on_release':self.add_member}]            
            self.current=name
        elif name=='change_pass_login':
            #CHANGE PASSWORD
            self.current='login'
        elif name=='create_fam_wallet':
            self.current='new_wallet'
            self.ids.new_wallet.ids.icon_fam.icon='check'
        elif name=='nointernet':
            self.current=name
            self.loop=Clock.schedule_interval(self.check_internet,1)
        elif name=='email':
            if os.path.exists(self.ids.picture.ids.image.source):
                self.data['Picture']=firebasetest.upload(self.ids.picture.ids.image.source)
                code=random.randint(1000,9999)
                res=self.email.verify_email(self.data['Email'],self.data['Name'],code)
                if res!='Unable to send Account Verification Code':
                    ans=app.digiconnect.verify_email_phone(self.data,code,'Email')
                    self.current=name
                    if ans=='Done':
                        self.show_remarks('The Code expires in 30 minutes',(1,1,1,1),'information')                        
                    else:
                        self.show_remarks(ans,(1,0,0,1),'alert')
                else:
                    self.show_remarks('Unable to send Account Verification Code',(1,0,0,1),'alert')
            else:
                self.show_remarks('File not found',(1,0,0,1),'alert')
        elif name=='phone':
            if not self.ids.email.ids.verifycod.text.strip().isdigit():
                self.show_remarks('No Code Inputed',(1,0,0,1))
            elif not 1000<=int(self.ids.email.ids.verifycod.text)<=9999:
                self.show_remarks('Incorrect Code Inputted',(1,0,0,1))
            code=random.randint(1000,9999)
            res=app.digiconnect.check_verify(int(self.ids.email.ids.verifycod.text.strip()),self.data['Email'],'Email')
            if res:
                ans=app.digiconnect.verify_email_phone(self.data,code,'Phone')
                if ans=='Done':                    
                    ans=app.digiapi.send_sms(f'+234{self.data["Phone"]}',f'Your Digi-Clini Verification Code: {code}')  
                    if ans:
                        self.show_remarks('SMS has been sent',(1,1,1,1),'information')                         
                        self.current=name
                    else:
                        self.show_remarks('Unable to send SMS',(1,0,0,0))
                else:
                    self.show_remarks(ans,(1,0,0,1),'alert')
                
            else:
                self.show_remarks('Invalid Code',(1,0,0,1))      
        elif name=='forgotpass':
            self.show_remarks('To be Included Soon',(1,1,1,1),'information')
        elif name=='new_wallet':
            if not self.ids.phone.ids.verifycod.text.strip().isdigit():
                self.show_remarks('No Code Inputed',(1,0,0,1))
            elif not 1000<=int(self.ids.phone.ids.verifycod.text)<=9999:
                self.show_remarks('Incorrect Code Inputed',(1,0,0,1))
            res=app.digiconnect.check_verify(int(self.ids.phone.ids.verifycod.text),self.data['Phone'],'Phone')
            if res:
                self.current=name
            else:
                self.show_remarks('Invalid Code',(1,0,0,1))    
        elif name=='savings':
            if self.ids.new_wallet.ids.icon_ind.icon=='check':
                self.current=name
            else:
                self.show_remarks('Create a Wallet',(1,0,0,1))
        elif name=='home':
            if self.ids.login.ids.user_email.text.strip()=='':
                self.show_remarks('Invalid Email',(1,0,0,1))
            elif self.ids.login.ids.password.text.strip()=='':
                self.show_remarks('Invalid Password',(1,0,0,1))
            try:
                a=encrypt.EnCrypt(self.ids.login.ids.password.text)
            except:
                self.show_remarks('Invalid Login Details',(1,0,0,1))
            if app.digiconnect.login(self.ids.login.ids.user_email.text,a.password()):
                self.current=name
            else:
                self.show_remarks('Incorrect Login Details',(1,0,0,1))
        elif name=='picture':
            gender=None
            if self.ids.personal.ids.male.active:
                gender='Male'
            if self.ids.personal.ids.female.active:
                gender='Female'
            self.data={'Name':f'{self.ids.personal.ids.fname.text.strip()} {self.ids.personal.ids.lname.text.strip()} {self.ids.personal.ids.oname.text.strip()}','Gender':gender,'DOB':self.ids.personal.ids.dob.text.strip(),'Real_DOB':self.ids.personal.ids.dob.date,'NIN':self.ids.personal.ids.nin.text.strip(),'Email':self.ids.personal.ids.email.text.strip(),'Phone':self.ids.personal.ids.phone.text.strip(),'Password':self.ids.personal.ids.password.text.strip(),'Confirm_Password':self.ids.personal.ids.confirm_password.text.strip(),'Street':self.ids.personal.ids.street.text.strip(),'State':self.ids.personal.ids.state.text.strip(),'Country':self.ids.personal.ids.country.text.strip()}
            if check.validate_personal(self.data)=='All Checked':
                self.current=name
            else:
                self.show_remarks(check.validate_personal(self.data),(1,0,0,1),'alert')
        elif name=='homebuild':
            res=app.digiconnect.book_new_user(self.data,app.now)
            self.current='home'
        elif name=='homebook':
            if self.ids.bioregister.ids.hospital.text=='Select Hospital':
                self.show_remarks('Select Hospital',(1,0,0,1))
            elif self.ids.bioregister.ids.date.text=='Select Date':
                self.show_remarks('Select Date',(1,0,0,1))
            elif self.ids.bioregister.ids.time.text=='Select Time':
                self.show_remarks('Select Time',(1,0,0,1))
            else:
                if app.digiconnect.book_new_user(self.data)=='Done':                
                    res=app.digiapi.create_wallet(self.data['Email'])
                    if res:
                        app.digiapi.verify_bvn(self.data['BVN'])
                    else:
                        #self.show_remarks('Unable to creat Wallet',(1,0,0,1))
                        pass
        else:
            self.current=name
    def custom_open(self,obj,text):
        if obj.md_bg_color==(1,1,1,1):
            text.disabled=True
        else:
            text.disabled=False
    def check_internet(self,dt):
        if app.now!='No Internet Connection':      
            self.loop.cancel()
    def open_hospital(self):        
        self.hospitalbuttom=HospitalButtom(screen=Factory.HospitalBox())             
        self.hospitalbuttom.open()        
        data=app.digiconnect.get_all_hospital()
        for i in data:
            self.hospitalbuttom.screen.ids.hospitalview.data.append(
            {
                'hospital':'HospitalList',
                'text':i["Name"],                
                'code':i["Hospital_Code"],
                'address':i['Address'],
                'icon':'hospital',
                'callback':lambda:self.change_hospital(self.ids.bioregister.ids.hospital,i['Name'],i['Hospital_Code'],self.hospitalbuttom),
                'on_release':lambda:self.change_hospital(self.ids.bioregister.ids.hospital,i['Name'],i['Hospital_Code'],self.hospitalbuttom)
                }
            )    
    def change_hospital(self,obj,name,code,bottom):
        bottom.dismiss()
        obj.text=name
        obj.code=code        
    def search_hospital(self,text):
        self.hospitalbuttom.screen.ids.hospitalview.data=[]
        data=app.digiconnect.get_all_hospital()
        for i in data:
            if text.lower()==i['Name']:
                self.hospitalbuttom.screen.ids.hospitalview.data.append(
                    {
                    'hospital':'HospitalList',
                    'text':i["Name"],                
                    'code':i["Hospital_Code"],
                    'address':i['Address'],
                    'icon':'hospital',
                    'callback':lambda:self.change_hospital(self.ids.bioregister.ids.hospital,i['Name'],i['Hospital_Code'],self.hospitalbuttom),
                    'on_release':lambda:self.change_hospital(self.ids.bioregister.ids.hospital,i['Name'],i['Hospital_Code'],self.hospitalbuttom)
                    }
                )           
        if self.hospitalbuttom.screen.ids.hospitalview.data==[]:
            self.hospitalbuttom.screen.ids.hospitalview.data=[{'hospital':'OneLineListItem','text':'No Registered Hospital with above name.'}]
    def option_choose(self,selected,*others):
        selected.md_bg_color=app.theme_cls.primary_dark
        if selected.value==0:            
            selected.textfield.disabled=False
        for i in others:
            i.md_bg_color=1,1,1,1  
            if i.value==0:
                i.textfield.disabled=True
    def option_daily(self,selected,*others):
        selected.md_bg_color=app.theme_cls.primary_dark
        for i in others:
            i.md_bg_color=1,1,1,1
    def open_dob(self):
        if app.now=='No Internet Connection':
            self.change_screen('nointernet')
        else:
            self.dob_picker=AKDatePicker(callback=self.change_dob,year_range=[app.now.year-150,app.now.year],now=app.now,title='SELECT DATE OF BIRTH')
            self.dob_picker.open()
    def open_appoint_date(self):
        if app.now=='No Internet Connection':
            self.change_screen('nointernet')
        else:
            self.appoint_date_picker=AKDatePicker(callback=self.change_appoint_date,year_range=[app.now.year,app.now.year+1,-1],now=datetime.datetime(app.now.year,app.now.month,app.now.day,app.now.hour,app.now.minute,app.now.second),title='SELECT DATE FOR APPOINTMENT')
            self.appoint_date_picker.open()
    def open_appoint_time(self):
        if app.now=='No Internet Connection':
            self.change_screen('nointernet')
        else:
            self.appoint_time_picker=MDTimePicker(title='SELECT TIME FOR APPOINTMENT')
            self.appoint_time_picker.on_save=self.change_appoint_time
            self.appoint_time_picker.open()    
    def change_appoint_time(self, time):
        self.ids.bioregister.ids.time.time=time
        self.ids.bioregister.ids.time.text=str(time.strftime('%H:%M:%S'))
        self.appoint_time_picker.dismiss()
    def change_dob(self,dt):
        if not dt:
            self.show_remarks('Invalid Date of Birth',(1,0,0,1),'alert')
        else:
            rem=app.now-datetime.datetime(dt.year,dt.month,dt.day,0,0,0)
            if rem.days<0:
                self.show_remarks('Incorrect Date of Birth',(1,0,0,1),'alert')
            else:
                self.ids.personal.ids.dob.date=dt
                self.ids.personal.ids.dob.text=self.get_date_text(dt)
        self.dob_picker.dismiss()
    def change_appoint_date(self,dt):
        if not dt:
            self.show_remarks('Invalid Date of Appointment',(1,0,0,1),'alert')
        else:
            if self.ids.bioregister.ids.time.text!='Select Time':
                dt=datetime.datetime(dt.year,dt.month.dt.day,self.ids.bioregister.ids.time.time.hour,self.ids.bioregister.ids.time.time.minute,self.ids.bioregister.ids.time.time.second)
            else:
                dt=datetime.datetime(dt.year,dt.month,dt.day,0,0,0)                
            self.ids.bioregister.ids.date.date=dt
            self.ids.bioregister.ids.date.text=self.get_date_text(dt)
        self.appoint_date_picker.dismiss()
    def choose_photo(self):
        path=filechooser.open_file()
        if len(path)==1:
            path=path[0]
            if os.path.splitext(path)[1] in ['.png','.ico','.jpg','.jpeg'] and os.path.getsize(path)<=1048576:
                self.ids.picture.ids.image.source=path
            else:
                if os.path.splitext(path)[1] not in ['.png','.ico','.jpg','.jpeg']:
                    self.show_remarks('Photo format must be .png, .jpeg or .ico',(1,0,0,1),'file-alert')
                else:
                    self.show_remarks('Photo maximum size is 1MB',(1,0,0,1),'image-broken-variant')                
        else:
            self.show_remarks('No Image selected',(1,0,0,1),'image-off')                    
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
    def change_password(self,obj,button):
        if button.text=='SHOW':
            obj.password=False
            button.text='HIDE'
        elif button.text=='HIDE':
            obj.password=True
            button.text='SHOW'
    def add_admin(self):
        box=MDBoxLayout(size_hint_y=None,height=dp(40))
        self.w=CupertinoTextField(hint_text='Enter Administrator ID',height=dp(10))
        c=MDFlatButton(text='CANCEL')
        s=MDRaisedButton(text='SUBMIT',md_bg_color=app.theme_cls.primary_light)
        box.add_widget(self.w)        
        self.a=MDDialog(title='Add Administrator',type='custom',content_cls=box,buttons=[c,s],height=dp(5))
        c.on_release=self.a.dismiss
        self.a.open()
    def add_member(self):
        box=MDBoxLayout(size_hint_y=None,height=dp(40))
        self.w=CupertinoTextField(hint_text='Enter Member ID',height=dp(10))
        c=MDFlatButton(text='CANCEL')
        s=MDRaisedButton(text='SUBMIT',md_bg_color=app.theme_cls.primary_light)
        box.add_widget(self.w)        
        self.a=MDDialog(title='Add Member',type='custom',content_cls=box,buttons=[c,s],height=dp(5))
        c.on_release=self.a.dismiss
        self.a.open()
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp,self).__init__(**kwargs)
        self.digiconnect=DigiSQL(host='localhost',user='root',password='0SE3050K0SUN')        
        self.digiapi=DigiClinicAPIS()        
        self.bg_color=1,1,1,1
        self.theme_cls.primary_palette='Green'
        self.now=datetime.datetime.now()
        #self.now=self.digiapi.get_time()
    def build(self):
        Window.size=(300,500)
        Window.top=50
        Window.left=50
        #DIMENSIONS
        #MULTITOUCH DISALLOWED
        pass
    def on_start(self):
        self.root.current='login'
if __name__=='__main__':
    app=MainApp()
    app.run()    