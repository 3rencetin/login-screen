import requests # type: ignore
import uuid

def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

def check_license():
    url = "http://your-server-ip:5000/check"  # Burada your-server-ip sunucu IP adresiniz olacak
    mac_id = get_mac_address()
    data = {"mac_id": mac_id}

    try:
        response = requests.post(url, json=data)
        result = response.json()

        if result["status"] == "registered":
            print("Welcome, registered user!")
            return True
        else:
            print(result["message"])
            return False
    except requests.RequestException as e:
        print(f"Error connecting to the server: {e}")
        return False

# Ana uygulama kodunuzun başında lisansı kontrol edin
if not check_license():
    print("Exiting application due to license check failure.")
    exit()

# Geri kalan uygulama kodunuz burada olacak