from Checker import *
from random import choice, choices, randint

def set_proxy(proxy:str=False):
    """
    Returns a proxy to use in requests
    Set a proxy to get a dictionary response

    set_proxy(proxy="127.0.0.1:5000")
    """
    if proxy:
        if proxy.count(':') == 3:
            host,port,username,password = proxy.split(':')
            proxy = f'{username}:{password}@{host}:{port}'

        match Checker.proxy_type:
            case "http": return {"http":f"http://{proxy}","https":f"http://{proxy}"}
            case "socks4": return {"http":f"socks4://{proxy}","https":f"socks4://{proxy}"}
            case "socks5": return {"http":f"socks5://{proxy}","https":f"socks5://{proxy}"}

    while 1:
        with Checker.proxy_lock:
            proxies = [proxy for proxy in Checker.proxies if proxy not in Checker.bad_proxies and proxy not in Checker.locked_proxies]
            if not proxies:
                Checker.bad_proxies.clear()
                continue
            proxy = choice(proxies)
            lock_proxy(proxy)
        return proxy
def return_proxy(proxy):
    """
    Remove a proxy from the locked proxies pool
    """
    with Checker.proxy_lock:
        if proxy in Checker.locked_proxies: Checker.locked_proxies.remove(proxy)
def lock_proxy(proxy):
    """
    Temporarily remove a proxy from the pool to lock to one thread
    """
    if Checker.lockProxies and proxy not in Checker.locked_proxies: Checker.locked_proxies.append(proxy)
def bad_proxy(proxy):
    """
    Temporarily remove a proxy from the pool for being bad
    """
    if proxy not in Checker.bad_proxies: Checker.bad_proxies.append(proxy)