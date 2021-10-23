import subprocess
import urllib.request
import pywifi
from pywifi import const
import time
import webbrowser


def get_netwoks():
    sid = "SSID"

    networks = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'])
    networks = networks.decode('ascii')
    networks = networks.replace('\r', '')
    networks_list = networks.split('\n')

    ssids = []

    for network in networks_list:
        if sid in network and 'BSSID' not in network:
            ssids.append(network[9:])

    print('WIFI networks aroud you:\n')
    for ssid in ssids:
        print(ssid)

    results = []
    SSID_list = networks.split("BSSID")
    for i in range(1, len(SSID_list)):
        temp = SSID_list[i]
        if (temp[1] == '1'):
            results.append([0])
        pos = 0
        if temp.find('Signal', pos) != -1:
            endingpos = temp.find('%', pos)
            pos = temp.find('Signal', pos)
            val = (temp[pos + 6:endingpos].replace(':', '').strip().replace('%', ''))
            val = int(val)
            if results[-1][0] < val:
                results[-1][0] = val

    max_val = 0
    max_index = 0
    for i in range(len(results)):
        if int(results[i][0]) > max_val:
            max_val = int(results[i][0])
            max_index = i
    print(ssids[max_index], 'is the strongest network around')
    connection = False

    while connection == False:
        try:
            password = input("Enter the password for " + ssids[max_index] + ' :')

            connect_to_wifi(ssids[max_index], password)
            connection = True
        except:
            print('error')


def check_conection():
    try:
        urllib.request.urlopen('https://google.com')
        return True
    except Exception as e:
        return False


def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)
    assert iface.status() in \
           [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(30)
    assert iface.status() == const.IFACE_CONNECTED


if __name__ == '__main__':
    get_netwoks()
    print('The network is connected to the internet' if check_conection() else 'Not intenet access')
    webbrowser.get().open_new('https://google.com/search?q=internet is working')
