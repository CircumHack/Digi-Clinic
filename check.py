def validate_personal(data):
    if not data['Name'].istitle():
        return 'Name must all be in titlecase'
    if data['Gender'] not in ['Male','Female']:
        return 'Select a Gender'
    if data['DOB']=='Select Date of Birth':
        return 'Select Date of Birth'
    if len(data['NIN'])!=11:
        return 'Invalid NIN'
    if len(data['Password'])<4:
        return 'Password must be minimum of 4 characters'
    if data['Password']!=data['Confirm_Password']:
        return 'Confirm your password correctly'
    if len(data['Email'])<10:
        return 'Invalid Email Address'
    if not(data['Email'][0].isalpha()):
        return 'Email must start with alphabets'
    e=False
    for i in ['gmail.com','yahoo.com','hotmail.com','aol.com','hotmail.co.uk','hotmail.fr','msn.com','yahoo.fr','wandoo.fr','orange.fr','comcast.net','yahoo.co.uk','yahoo.com.br','yahoo.co.in','live.com','rediffmail.com','free.fr','gmx.de','web.de','yandex.ru','ymail.com','libero.it','outlook.com','uol.com.br','bol.com.br','mail.ru','cox.net','hotmail.it','sbcglobal.net','sfr.fr','live.fr','verizon.net','live.co.uk','googlemail.com','yahoo.es','ig.com.br','live.nl','bigpond.com','terra.com.br','yahoo.it','neuf.fr','yahoo.de','alice.it','rocketmail.com','att.et','laposte.net','facebook.com','bellsouth.net','yahoo.in','hotmail.es','charter.net','yahoo.ca','yahoo.com.au','rambler.ru','hotmail.de','tiscali.it','shaw.ca','yahoo.co.jp','sky.com','earthlink.net','optonline.net','freenet.de','t-online.de','aliceadsl.fr','virgilio.it','home.nl','qq.com','telnet.be','me.com','yahoo.com.ar','tiscali.co.uk','yyahoo.com.mx','voila.fr','gmx.net','mail.com','planet.nl','tin.it','live.it','ntlworld.com','arcor.de','yahoo.co.id','frontiernet.net','hetnet.nl','live.com.au','yahoo.com.sg','zonnet.nl','club-internet.fr','juno.com','optusnet.com.au','blueyonder.co.uk','bluewin.ch','skynet.be','sympatico.ca','windstream.net','mac.com','centurytel.net','chello.nl','live.ca','aim.com','bigpond.net.au']:
        if data['Email'].endswith(i):
            e=True
            break
    if not e:
        return 'Wrong Email Domain Name'    
    if len(data['Phone']) not in [11,12,13]:
        return 'Invalid Phone Number'
    if len(data['Street'])<8:
        return 'Street line must be minimum of 8 characters'
    if len(data['State'])<8:
        return 'State must be minimum of 8 characters'
    return 'All Checked'