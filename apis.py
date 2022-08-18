import requests,json,datetime
sandboxkey='EgHfwkCzCCiGdIAmyca3CpEij3uGtv3f1659282153'
flutterwave_public_key='FLWPUBK_TEST-94cf386296fc787757d3fe69e6e8d1e1-X'
flutterwave_secret_key='FLWSECK_TEST-9b70859a0c90a05fa2c5a379df072a2b-X'
encryption_key='FLWSECK_TESTa2e6ec49862a'
from rave_python import Rave
from rave_python.rave_virtualaccount import VirtualAccount
#africastalking_username='digiclinic'
#africastalking_api_key='62beb14f610058a0eff24526654d4f685fafb51761217e39ad399705a7cfbbc8'
#

class DigiClinicAPIS:
    def __init__(self):
        self.send_sms_url="https://fsi.ng/api/v1/africastalking/version1/messaging"
        self.verify_bvn_url="https://fsi.ng/api/bvnr/VerifySingleBVN"
        self.create_wallet_url="https://fsi.ng/api/v1/flutterwave/v3/virtual-account-numbers"
        self.create_card_url="https://fsi.ng/api/v1/flutterwave/v3/virtual-cards"
        self.verify_one_bvn_url = "https://fsi.ng/api/bvnr/VerifySingleBVN"
        self.encrypt_bvn="https://fsi.ng/api/bvnr/encrypt"
        self.rave=Rave(flutterwave_public_key,secretKey=flutterwave_secret_key,production=False,usingEnv=False)
    def send_sms(self,reciever,message):
        data=json.dumps({'username':'sandbox','to':reciever,'message':message})
        head={'sandbox-key':sandboxkey,'Content-Type':'application/json'}
        response=requests.request('POST',self.send_sms_url,headers=head,data=data)
        response=json.loads(response.content)
        if response['SMSMessageData']['Recipients'][0]['status']=='Success':
            return True
        return False
    def bvn_encrypt(self,num):
        payload = json.dumps({"BVNS": num})
        headers = {'Accept': 'application/json','Content-Type': 'application/json','Sandbox-key': sandboxkey}
        response = requests.request("POST", self.encrypt_bvn, headers=headers, data=payload)
        return response.text
    def verify_bvn(self,bvn):
        encrypt=self.bvn_encrypt(bvn)
        payload = json.dumps(encrypt)
        headers = {'Accept': 'application/json','Content-Type': 'application/json','Sandbox-key': sandboxkey}
        response = requests.request("POST", self.verify_one_bvn_url, headers=headers, data=payload)
        return response.text
    def create_wallet(self,email):
        try:
            res=VirtualAccount(flutterwave_public_key,flutterwave_secret_key,production=False,usingEnv=False)
            res.create({
            "email": email,
            "seckey": flutterwave_secret_key,
            "is_permanent": True,
            "narration":"Creation of Digi-Clinic Account"
            })
            if res['status']=='Success':
                 #create card
                return res
            return False
        except:
            return False
    def get_address(self):
        if self.geolocator.status=='OK' and self.geolocator.status_code==200:
            data=self.geolocator.geojson
            return {'Address':data['features'][0]['properties']['address'],'City':data['features'][0]['properties']['city'],'Country':data['features'][0]['properties']['country'],'IP':data['features'][0]['properties']['ip'],'Longitude':data['features'][0]['properties']['lng'],'Latitude':data['features'][0]['properties']['lat'],'State':data['features'][0]['properties']['state']}        

#a=DigiClinicAPIS()
#print(a.send_sms('+2348033245362','Hello'))
#print(a.verify_bvn('039290339390'))
a=DigiClinicAPIS()
print(a.create_wallet('circumokosun@gmail.com'))