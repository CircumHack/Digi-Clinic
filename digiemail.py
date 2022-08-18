from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,ssl

class EmailSender:
    def __init__(self):
        self.sender='circumokosun@gmail.com'        
        self.password='dfqrmpgzlxsslvrb'
        self.message=MIMEMultipart()
        self.context=ssl.create_default_context()
    def verify_email(self,reciever_email,reciever_name,code):
        try:            
            self.message['Subject']='Email Verification - Digi Clinic' 
            self.message['From']=self.sender
            self.message['To']=reciever_email
            html=f'''
                <html>
                    <body>
                        <center><p>Hi {reciever_name},<br/><br/>
                        The code below is your verification code for your Digi Clinic account.<br/>
                        <h3><b>{code}</b><br/></h3>
                        Note: This code expires in 30 minutes.<br/>
                        <font color="#ff0000"><b>Please don\'t share this code with anyone for security purposes.</b></font><br/>
                        If you have any issue check out on our website: <a href="http://www.fsi.ng">FAQ</a> page.<br/><br/>
                        Thanks,<br/>
                        Digi-Clinic Team.
                        </p></center>
                    </body>
                </html>'''
            htmlpart=MIMEText(html,'html')        
            self.message.attach(htmlpart)
            with smtplib.SMTP_SSL("smtp.gmail.com",465,context=self.context) as server:
                server.login(self.sender,self.password)
                server.sendmail(self.sender,reciever_email,self.message.as_string())
            return code
        except:
            return 'Unable to send Account Verification Code'
    def send_username(self,reciever_email,reciever_name,usern):
        try:            
            self.message['Subject']='Login Details - MyStore' 
            self.message['From']=self.sender
            self.message['To']=reciever_email
            html=f'''
                <html>
                    <body>
                        <center><p>Hi {reciever_name},<br/><br/>
                        You have successfully created your MyStore account.<br/>
                        <h5>Your Username is <b>{usern}</b><br/></h3><br/>
                        <button><a href="https://www.google.com"><font color="#0000ff"><b>Click to Change Password.</b></font></a></button><br/>
                        For more update check out our <a href="http://www.google.com">FAQ</a> page.<br/><br/>
                        
                        Thanks,<br/>
                        MyStore Team.
                        </p></center>
                    </body>
                </html>'''
            htmlpart=MIMEText(html,'html')        
            self.message.attach(htmlpart)
            with smtplib.SMTP_SSL("smtp.gmail.com",465,context=self.context) as server:
                server.login(self.sender,self.password)
                server.sendmail(self.sender,reciever_email,self.message.as_string())
            return usern
        except:
            return 'Unable to send Details'
    def send_password_access_code(self,reciever_email,reciever_name,key):
        try:            
            self.message['Subject']='Change Password - MyStore' 
            self.message['From']=self.sender
            self.message['To']=reciever_email
            html=f'''
                <html>
                    <body>
                        <center><p>Hi {reciever_name},<br/><br/>
                        You requested for a change of password for your MyStore account.<br/>
                        The code below is your access key.<br/>
                        <h3><b>{key}</b><br/></h3>
                        <font color="#ff0000"><b>Please don\'t share this code with anyone for security purposes.</b></font><br/>
                        To report any case of abnormality call our helpline +234708488650.<br/><br/>
                        Thanks,<br/>
                        MyStore Team.
                        </p></center>
                    </body>
                </html>'''
            htmlpart=MIMEText(html,'html')        
            self.message.attach(htmlpart)
            with smtplib.SMTP_SSL("smtp.gmail.com",465,context=self.context) as server:
                server.login(self.sender,self.password)
                server.sendmail(self.sender,reciever_email,self.message.as_string())
            return key
        except:
            return 'Unable to send Access Key'