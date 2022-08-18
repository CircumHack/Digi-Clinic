import random
class EnCrypt:
    def __init__(self,inp:str):
        if str(len(inp)**0.5).split('.')[1]!='0':
            for i in range(int(len(inp)**0.5),len(inp)+1):
                if str(int(len(inp)+i)**0.5).split('.')[1]=='0':
                    break
            inp+='0'*i
        matr=[]
        self.inp=inp
        x=int(len(inp)**0.5)
        if x==0:
            x=1
        y=len(inp)+int(len(inp)**0.5)
        if y==0:
            y=1
        z=int(len(inp)**0.5)
        if z==0:
            z=1
        for i in range(x,y,z):            
            matr.append(list(inp[i-int(len(inp)**0.5):i]))
        trmat=list(zip(*matr))
        trstr=''.join(sum(trmat,()))
        self.data={
            'a':'G',
            'b':' ',
            'c':'3',
            'd':'U',
            'e':'z',
            'f':'A',
            'g':'b',
            'h':'v',
            'i':'0',
            'j':'B',
            'k':'9',
            'l':'5',
            'm':'u',
            'n':'H',
            'o':'4',
            'p':'K',
            'q':'p',
            'r':'c',
            's':'k',
            't':'N',
            'u':'F',
            'v':'Q',
            'w':'2',
            'x':'g',
            'y':'E',
            'z':'j',
            'A':'O',
            'B':'s',
            'C':'8',
            'D':'V',
            'E':'S',
            'F':'l',
            'G':'X',
            'H':'f',
            'I':'D',
            'J':'t',
            'K':'1',
            'L':'R',
            'M':'a',
            'N':'7',
            'O':'o',
            'P':'W',
            'Q':'T',
            'R':'w',
            'S':'h',
            'T':'Y',
            'U':'e',
            'V':'J',
            'W':'L',
            'X':'m',
            'Y':'q',
            'Z':'i',
            '0':'P',
            '1':'M',
            '2':'C',
            '3':'I',
            '4':'6',
            '5':'y',
            '6':'n',
            '7':'x',
            '8':'r',
            '9':'d',
            ' ':'Z',
        }
        self.num={
            'a':'20',
            'b':'39',
            'c':'23',
            'd':'48',
            'e':'08',
            'f':'12',
            'g':'57',
            'h':'47',
            'i':'26',
            'j':'17',
            'k':'32',
            'l':'29',
            'm':'40',
            'n':'13',
            'o':'56',
            'p':'49',
            'q':'25',
            'r':'02',
            's':'38',
            't':'22',
            'u':'09',
            'v':'50',
            'w':'34',
            'x':'04',
            'y':'31',
            'z':'16',
            'A':'41',
            'B':'53',
            'C':'43',
            'D':'37',
            'E':'62',
            'F':'11',
            'G':'28',
            'H':'03',
            'I':'60',
            'J':'21',
            'K':'52',
            'L':'42',
            'M':'33',
            'N':'14',
            'O':'24',
            'P':'46',
            'Q':'55',
            'R':'01',
            'S':'51',
            'T':'30',
            'U':'44',
            'V':'58',
            'W':'15',
            'X':'06',
            'Y':'61',
            'Z':'35',
            '0':'45',
            '1':'18',
            '2':'54',
            '3':'05',
            '4':'59',
            '5':'19',
            '6':'36',
            '7':'07',
            '8':'63',
            '9':'27',
            ' ':'10',
        }
        self.other={
            'a':'20',
            'b':'39',
            'c':'23',
            'd':'48',
            'e':'08',
            'f':'12',
            'g':'57',
            'h':'67',
            'i':'26',
            'j':'17',
            'k':'32',
            'l':'29',
            'm':'40',
            'n':'13',
            'o':'56',
            'p':'49',
            'q':'25',
            'r':'02',
            's':'38',
            't':'22',
            'u':'09',
            'v':'50',
            'w':'34',
            'x':'04',
            'y':'31',
            'z':'16',
            'A':'41',
            'B':'53',
            'C':'43',
            'D':'37',
            'E':'62',
            'F':'11',
            'G':'28',
            'H':'03',
            'I':'60',
            'J':'21',
            'K':'52',
            'L':'42',
            'M':'33',
            'N':'14',
            'O':'24',
            'P':'46',
            'Q':'55',
            'R':'01',
            'S':'51',
            'T':'30',
            'U':'44',
            'V':'58',
            'W':'15',
            'X':'06',
            'Y':'61',
            'Z':'35',
            '0':'45',
            '1':'18',
            '2':'54',
            '3':'05',
            '4':'59',
            '5':'19',
            '6':'36',
            '7':'07',
            '8':'63',
            '9':'27',
            ' ':'10',
            '~':'68',
            '!':'81',
            '@':'72',
            '#':'65',
            '$':'96',
            '%':'83',
            '^':'93',
            '&':'74',
            '*':'70',
            '(':'89',
            ')':'82',
            '_':'79',
            '+':'98',
            '`':'86',
            '-':'75',
            '=':'91',
            '{':'94',
            '}':'87',
            '[':'71',
            ']':'99',
            '\\':'95',
            '|':'64',
            ':':'80',
            ';':'66',
            '\'':'97',
            '"':'78',
            '<':'92',
            '>':'69',
            ',':'90',
            '.':'00',
            '/':'73',
            '?':'84',
        }
        self.swap=''
        for i in trstr:
            self.swap+=self.other[i]              
    def shop_id(self):
        v=''
        for i in self.swap:
            v+=self.num[i]
        self.sans=self.inp[:3].upper()+v[:7]
        if len(self.sans)<10:
            self.swap+=' '*(10-len(self.sans))
            for i in self.swap:
                  v+=self.other[i]
            self.sans=self.inp[:3].upper()+v[:7]
        return ('BRANCH'+self.sans).upper()
    def person_id(self,pid:str):        
        self.sn=''
        self.p=''
        for i in pid:
            self.p+=self.num[self.data[i]]
        for i in self.swap+self.p:                  
            self.sn+=self.num[i]
        self.cutoff=self.sn[:len(self.sn)-(len(self.sn)%12)]
        self.v=[] 
        for i in range(len(self.cutoff)//12,len(self.cutoff),len(self.cutoff)//12):
            self.v.append(self.cutoff[i-len(self.cutoff)//12:i])
        self.ans=''
        for i in range(1,len(self.v)+1):
            if i%2==0:
                self.ans+=str(max(list(map(int,list(self.v[i-1])))))
            else:
                self.ans+=str(min(list(map(int,list(self.v[i-1])))))
        w=pid.split()
        w=w[0][0]+w[1][0]+w[2][0]
        d=(('USER'+w+self.ans[::-2])[:13]).upper()
        if len(d)<20:
            for i in range(20-len(d)):
                d+=str(random.randint(0,9))
        return d[:20]
    def role_id(self,role:str,shop:str):
        v=''
        for i in role[::-1]:
            v+=self.num[self.data[i]]
        return ('ROLE'+shop[:3].upper()+role[:3].upper()+v[:10]).upper()
    def password(self):
        v=''
        for i in self.swap:
            v+=self.num[i]
        w=''
        for i in range(0,len(v),2):
            w+=v[i:i+2][::-1]
        if w=='':
            w='0'
        b=bin(int(w))[2:]
        ans=''
        for i in b:
            if i=='0':
                ans+='1'
            else:
                ans+='0'
        return ans
    def get_cat_id(self,cname:str,sid:str):
        c=''
        for i in cname[3:]:
            c+=self.num[i]
        if len(c)<10:
            for i in range(10-len(c)):
                c+=str(random.randint(0,9))
        else:
            c=c[:10]
        return (sid[:3].upper()+cname[:3].upper()+c).upper()
    def get_prod_id(self,pname:str,sid:str):
        if len(pname)%2==1:
            pname+=' '
        p=''
        for i in range(0,len(pname),2):
            p+=pname[i+1]
            p+=pname[i]
        c=''
        for n in p:
            c+=self.num[self.data[n]]
        return (('PRODUCT'+sid[:3].upper()+pname[:4].upper()+c)[:20]).upper()
class DeCrypt:
    def __init__(self,inp:str):
        reans=''
        for i in inp:
            if i=='0':
                reans+='1'
            else:
                reans+='0'
        dec=str(int(reans,2))  
        self.ex=''
        for i in range(0,len(dec),2):
            self.ex+=dec[i:i+2][::-1]
    def decipher(self):
        self.data={
        'G':'a',
        ' ':'b',
        '3':'c',
        'U':'d',
        'z':'e',
        'A':'f',
        'b':'g',
        'v':'h',
        '0':'i',
        'B':'j',
        '9':'k',
        '5':'l',
        'u':'m',
        'n':'H',
        '4':'o',
        'K':'p',
        'p':'q',
        'c':'r',
        'k':'s',
        'N':'t',
        'F':'u',
        'Q':'v',
        '2':'w',
        'g':'x',
        'E':'y',
        'j':'z',
        'O':'A',
        's':'B',
        '8':'C',
        'V':'D',
        'S':'E',
        'l':'F',
        'X':'G',
        'f':'H',
        'D':'I',
        't':'J',
        '1':'K',
        'R':'L',
        'a':'M',
        '7':'N',
        'o':'O',
        'W':'P',
        'T':'Q',
        'w':'R',
        'h':'S',
        'Y':'T',
        'e':'U',
        'J':'V',
        'L':'W',
        'm':'X',
        'q':'Y',
        'i':'Z',
        'P':'0',
        'M':'1',
        'C':'2',
        'I':'3',
        '6':'4',
        'y':'5',
        'n':'6',
        'x':'7',
        'r':'8',
        'd':'9',
        'Z':' ',
        }
        self.num={
            '20':'a',
            '39':'b',
            '23':'c',
            '48':'d',
            '08':'e',
            '12':'f',
            '57':'g',
            '47':'h',
            '26':'i',
            '17':'j',
            '32':'k',
            '29':'l',
            '40':'m',
            '13':'n',
            '56':'o',
            '49':'p',
            '25':'q',
            '02':'r',
            '38':'s',
            '22':'t',
            '09':'u',
            '50':'v',
            '34':'w',
            '04':'x',
            '31':'y',
            '16':'z',
            '41':'A',
            '53':'B',
            '43':'C',
            '37':'D',
            '62':'E',
            '11':'F',
            '28':'G',
            '03':'H',
            '60':'I',
            '21':'J',
            '52':'K',
            '42':'L',
            '33':'M',
            '14':'N',
            '24':'O',
            '46':'P',
            '55':'Q',
            '01':'R',
            '51':'S',
            '30':'T',
            '44':'U',
            '58':'V',
            '15':'W',
            '06':'X',
            '61':'Y',
            '35':'Z',
            '45':'0',
            '18':'1',
            '54':'2',
            '05':'3',
            '59':'4',
            '19':'5',
            '36':'6',
            '07':'7',
            '63':'8',
            '27':'9',
            '10':' ',
        }
        self.other={
            '20':'a',
            '39':'b',
            '23':'c',
            '48':'d',
            '08':'e',
            '12':'f',
            '57':'g',
            '67':'h',
            '26':'i',
            '17':'j',
            '32':'k',
            '29':'l',
            '40':'m',
            '13':'n',
            '56':'o',
            '49':'p',
            '25':'q',
            '02':'r',
            '38':'s',
            '22':'t',
            '09':'u',
            '50':'v',
            '34':'w',
            '04':'x',
            '31':'y',
            '16':'z',
            '41':'A',
            '53':'B',
            '43':'C',
            '37':'D',
            '62':'E',
            '11':'F',
            '28':'G',
            '03':'H',
            '60':'I',
            '21':'J',
            '52':'K',
            '42':'L',
            '33':'M',
            '14':'N',
            '24':'O',
            '46':'P',
            '55':'Q',
            '01':'R',
            '51':'S',
            '30':'T',
            '44':'U',
            '58':'V',
            '15':'W',
            '06':'X',
            '61':'Y',
            '35':'Z',
            '45':'0',
            '18':'1',
            '54':'2',
            '05':'3',
            '59':'4',
            '19':'5',
            '36':'6',
            '07':'7',
            '63':'8',
            '27':'9',
            '10':' ',
            '68':'~',
            '81':'!',
            '72':'@',
            '65':'#',
            '96':'$',
            '83':'%',
            '93':'^',
            '74':'&',
            '70':'*',
            '89':'(',
            '82':')',
            '79':'_',
            '98':'+',
            '86':'`',
            '75':'-',
            '91':'=',
            '94':'{',
            '87':'}',
            '71':'[',
            '99':']',
            '95':'\\',
            '64':'|',
            '80':':',
            '66':';',
            '97':'\'',
            '78':'"',
            '92':'<',
            '69':'>',
            '90':',',
            '00':'.',
            '73':'/',
            '84':'?',
        }
        self.swap=''
        for i in range(0,len(self.ex),2):
            self.swap+=self.num[self.ex[i:i+2]]
        trstr=''
        for i in range(0,len(self.swap),2):
            trstr+=self.other[self.swap[i:i+2]]
        trmat=[]
        for i in range(0,len(trstr),int(len(trstr)**0.5)):
            trmat.append(list(trstr[i:i+int(len(trstr)**0.5)]))
        self.matr=list(zip(*trmat))
        self.ans=''.join(sum(self.matr,()))
        return self.ans