from threading import Lock

lock = Lock()

class Checker:
    bad = 0
    good = 0
    custom = 0
    cpm = 0
    cpm_averages = [0]
    errors = 0

    checking = False
    proxies = []
    locked_proxies = []
    bad_proxies = []
    accounts = []
    remaining = []
    total_proxies = 0
    total_accounts = 0
    time = ""

    solver_serice = '2captcha'
    api_key = ''

    lockProxies = False
    cui = True
    retries = 1
    timeout = 10
    threads = 200
    proxy_type = "http"
    
    proxy_lock = Lock()
    save_lock = Lock()
    print_lock = Lock()