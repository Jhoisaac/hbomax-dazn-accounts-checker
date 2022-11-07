from tkinter import Tk,filedialog
from Checker import *
from proxies import *
from modules.dazn import *
from modules.hbomax import *

def get_file(title:str,type:str):
    """
    Gets a filepath
    Returns False if nothing was given
    get_file(title="Combo File",type="Combo File")
    """
    root = Tk()
    root.withdraw()
    root.lift()
    #root.iconbitmap(default=ICON_PATH)
    response = filedialog.askopenfilename(title=title,filetypes=((type, '.txt'),('All Files', '.*'),))
    root.destroy()
    return response if response not in ("",()) else False

print('𝒮☯𝒩𝒦 𝒟𝒜𝒵𝒩 𝒞𝐻𝐸𝒞𝒦𝐸𝑅')

print('[1] DAZN   [2] HBOMAX:')
qchecker = 2
print(qchecker)

file_path_trys = 0
file_path = False
while file_path == False:
    file_path = get_file("Combo File",type="Combo File")
    file_path_trys=file_path_trys+1
    if file_path_trys >= 3:
        print('ERROR - You must select a Combo File')
        quit()

fileproxies_path_trys = 0
fileproxies_path = False
while fileproxies_path == False:
    fileproxies_path = get_file("Proxy File",type="Proxy File")
    file_path_trys=file_path_trys+1
    with open(fileproxies_path,errors="ignore") as file:
            before_proxies = file.read().splitlines()
            after_proxies = list(set(before_proxies))
            Checker.proxies = after_proxies
            Checker.total_proxies = len(Checker.proxies)
            duplicates = len(before_proxies)-len(after_proxies)
    if fileproxies_path_trys >= 3:
        print('ERROR - You must select a Combo File')
        quit()

   
file = open(file_path,errors="ignore")

for i in file:
    seq = i.strip()
    acc = seq.split(':')
    if qchecker == 1:
        DAZN_Check(acc[0],acc[1])   
    else:
        HBOMAX_Check(acc[0],acc[1])