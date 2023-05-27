import os
import requests
import time
import random

print('''
╦╦╔═╗ ╦ ╦╔═╗╔╗   ┌─┐┌─┐┌─┐┌┐┌┌┐┌┌─┐┬─┐
║║╚═╗ ║║║║╣ ╠╩╗  └─┐│  ├─┤││││││├┤ ├┬┘
╩╩╚═╝o╚╩╝╚═╝╚═╝  └─┘└─┘┴ ┴┘└┘┘└┘└─┘┴└─
IIS SCANNER USE IP
 ./IIS_NEW.txt''')

def CHECKING():
    IIS = []
    TIMEOUT = []

    with open(os.path.join(os.path.dirname(__file__), 'IIS.txt'), 'r') as f:
        d = f.readlines()
        for IP_IIS in d:
            IP = IP_IIS.replace('\n', '').replace('http://', '').replace('/', '')
            if IP not in IIS:
                IIS.append(IP)
                print(f'NEW IP {IP} OF {len(IIS)}')

    print('\nCHECKING TIMEOUT OF IIS . . .')
    for IP_WEB in IIS:
        try:
            time_s = time.time()
            r = requests.get(f'http://{IP_WEB}', timeout=3)
            time_e = time.time()
            ms = int((time_e - time_s) * 1000)
            if r.status_code == 200:
                TIMEOUT.append(f'{IP_WEB}|{ms}')
                print(f"200 OK OF {IP_WEB} MS={ms}")
        except requests.Timeout:
            print(f"TIMEOUT OF {IP_WEB}")
        except requests.RequestException as e:
            print(f"ERROR: {str(e)}")

    print('\nALL MS OF IP')
    for i in TIMEOUT:
        print(i)

def FIND_CONTENT_IIS7():
    content_IIS7_html = []
    content_IIS8_html = []
    content_IIS10_html = []
    IIS_ALL = []
    WEBSITE = []
    IP_CONTENT = []
    count = 0
    with open(os.path.join(os.path.dirname(__file__), 'IIS.txt'), 'r') as f:
        d = f.readlines()
        for IP_IIS in d:
            IP = IP_IIS.replace('\n', '')
            try:
                r = requests.get(f'{IP}', timeout=3)
                if r.status_code == 200:
                    if IP not in IP_CONTENT:
                        IP_CONTENT.append(IP)
                        if r.content not in content_IIS7_html:
                            if b'<title>IIS7</title>' in r.content:
                                count += 1
                                print(f"URL={IP} PAGE={count} NEW CONTENT IIS7")
                                content_IIS7_html.append(r.content)
                            elif b'<title>IIS Windows Server</title>' in r.content:
                                count += 1
                                print(f"URL={IP} PAGE={count} NEW CONTENT IIS10")
                                content_IIS10_html.append(r.content)
                            else:
                                count += 1
                                print(f"URL={IP} PAGE={count} NEW CONTENT IIS8")
                                content_IIS8_html.append(r.content)
            except requests.Timeout:
                if IP not in IP_CONTENT:
                    IP_CONTENT.append(IP)
                    print(f"URL={IP} DOWN . . .")
            except requests.RequestException as e:
                print(f"ERROR: {str(e)}")

    IP_MODE = input("MODE IIS OR ALL?")
    TIMEOUT_SET = int(input("TIMEOUT 3 (old) ?"))

    while True:
        if IP_MODE.upper() == 'IIS':
            IP = f'{random.randint(3, 217)}.{random.randint(0, 247)}.{random.randint(29, 219)}.{random.randint(4, 255)}'
        else:
            IP = f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'

        try:
            r = requests.get(f'http://{IP}', timeout=TIMEOUT_SET)
            if r.status_code == 200:
                if r.content in content_IIS7_html:
                    if IP not in IIS_ALL:
                         if IP not in IP_CONTENT:
                             IIS_ALL.append(IP)
                             print(f"{IP} IIS7 FOUND (CONTENT)")
                elif r.content in content_IIS10_html:
                    if IP not in IIS_ALL:
                         if IP not in IP_CONTENT:
                             IIS_ALL.append(IP)
                             print(f"{IP} IIS10 FOUND (CONTENT)")
                elif r.content in content_IIS8_html:
                    if IP not in IIS_ALL:
                         if IP not in IP_CONTENT:
                             IIS_ALL.append(IP)
                             print(f"{IP} IIS8 FOUND (CONTENT)")
                else:
                    if b'<title>IIS7</title>' == r.content:
                        if IP not in IIS_ALL:
                         if IP not in IP_CONTENT:
                             IIS_ALL.append(IP)
                             print(f'{IP} IIS7 FOUND (NEW CONTENT)')
                             content_IIS7_html.append(r.content)
                        break
                    elif b'<title>IIS Windows Server</title>' == r.content:
                        content_IIS10_html.append(r.content)
                        if IP not in IIS_ALL:
                         if IP not in IP_CONTENT:
                             IIS_ALL.append(IP)
                             print(f'{IP} IIS10 FOUND (NEW CONTENT)')
                    elif b'<title>ARR - Microsoft Internet Information Services 8</title>' == r.content or b'<title>Microsoft Internet Information Services 8 - SSRS 01 - 71</title>' == r.content or b'<title>SRV-WS Microsoft Internet Information Services 8</title>' == r.content or b'<title>Microsoft Internet Information Services 8-cwn</title>' == r.content:
                        content_IIS8_html.append(r.content)
                        if IP not in IIS_ALL:
                         if IP not in IP_CONTENT:
                             IIS_ALL.append(IP)
                             print(f'{IP} IIS8 FOUND (NEW CONTENT)')
                    else:
                        WEBSITE.append(IP)
                        print(f"{IP} NORMAL PAGE WEBSITE . . .")
            else:
                if r.status_code == 404:
                    print(f"{IP} STATUS NOT FOUND . . .")
                elif r.status_code == 403:
                    print(f"{IP} STATUS BLOCK . . .")
                else:
                    print(f"{IP} OTHER STATUS CODE . . .")
        except KeyboardInterrupt:
            with open(os.path.join(os.path.dirname(__file__), 'IIS_SCAN.txt'), 'a') as f:
                for I in IIS_ALL:
                    f.write(f'{I}\n')
            with open(os.path.join(os.path.dirname(__file__), 'NORMAL_SCAN.txt'), 'a') as f:
                for I in WEBSITE:
                    f.write(f'{I}\n')
            break
        except requests.Timeout:
            print(f"TIMEOUT OF {IP}")
        except requests.RequestException as e:
            print(f'ERROR OF {IP}')
CHECKING()
FIND_CONTENT_IIS7()
