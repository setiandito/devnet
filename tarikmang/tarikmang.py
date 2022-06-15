from netmiko import ConnectHandler
import os
import re
from getpass import getpass

print("""
████████╗░█████╗░██████╗░██╗██╗░░██╗░░░░░░███╗░░░███╗░█████╗░███╗░░██╗░██████╗░
╚══██╔══╝██╔══██╗██╔══██╗██║██║░██╔╝░░░░░░████╗░████║██╔══██╗████╗░██║██╔════╝░
░░░██║░░░███████║██████╔╝██║█████═╝░█████╗██╔████╔██║███████║██╔██╗██║██║░░██╗░
░░░██║░░░██╔══██║██╔══██╗██║██╔═██╗░╚════╝██║╚██╔╝██║██╔══██║██║╚████║██║░░╚██╗
░░░██║░░░██║░░██║██║░░██║██║██║░╚██╗░░░░░░██║░╚═╝░██║██║░░██║██║░╚███║╚██████╔╝
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░░░░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░

 Export Config Cisco-IOS via SSH
 by setiandito
 masukkan IPv4 perangkat pada file listip.txt
    """)
    
with open("listip.txt", "r") as tf:
    listip = tf.read().split('\n')
    tf.close()
jumlah = len(listip)
cek = ""
while cek != "Y" or cek != "y" or cek != "T" or cek != "t":
    cek = input("Apakah ingin menampilkan list-ip ? (Y/T) :")
    
    if cek == "Y" or cek == "y":
        for i in range (jumlah) :
            print(f"[{i+1}/{jumlah}]  - "+listip[i])
        break
    elif cek == "T" or cek == "t":
        break
print(f"Total Perangkat: {jumlah}")

user = input("SSH_login as: ")
password = getpass("SSH_password: ")
secret = getpass("Secret [bisa dikosongin jika tidak ada]: ")
for ip in listip:

    cisco = {
        'device_type':'cisco_ios',
        'ip':ip,
        'username':user,
        'password':password,
        'secret':secret
        }

    conn = ConnectHandler(**cisco)
    try:
        enable = conn.enable()
        print("SSH:Connect to "+ip)
        run_conf = conn.send_command('show running-config')
        hostname = re.search("hostname(.*)\s",run_conf).group(0).split(" ")
        namefile = ("exp_cfg-{}.txt".format(hostname[1].replace("\n","")))
        folder = "config"
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        path = os.path.join(f".\{folder}", namefile)
        file = open(path, "w")
        file.write(run_conf)
        file.close()
        print(f"Selesai, config disimpan di {path}")
    except:
      print("Error")

