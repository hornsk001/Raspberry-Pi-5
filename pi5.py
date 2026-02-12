#!/usr/bin/env python3
import subprocess, platform, glob, os

# Konfiguration
V, REPO = "0.2", "https://github.com/hornsk001/Raspberry-Pi-5"
W = 56 # Konstante Innenbreite

# Farben
Y = '\033[1;33m'
G = '\033[0;32m'
B = '\033[0;34m'
N = '\033[0m'

def get(c):
    try: return subprocess.check_output(c, shell=True).decode().strip()
    except: return "N/A"

def get_nvme():
    for p in glob.glob("/sys/class/hwmon/hwmon*/temp1_input"):
        try:
            with open(os.path.join(os.path.dirname(p), "name")) as f:
                if "nvme" in f.read():
                    with open(p) as tf: return f"{int(tf.read())/1000:.1f} C"
        except: continue
    return "N/A"

# Daten sammeln
hw = open("/proc/device-tree/model").read().strip('\0')
kn = platform.release()
ct = get("vcgencmd measure_temp").replace("temp=","").replace("'C"," C")
nt = get_nvme()
cf = f"{float(get('vcgencmd measure_clock arm').split('=')[1] or 0)/10**9:.2f} GHz"
vc = get("vcgencmd measure_volts core").split('=')[1] if '=' in get("vcgencmd measure_volts core") else "N/A"
fn = f"{get('cat /sys/class/hwmon/hwmon*/fan1_input 2>/dev/null | head -n1') or '0'} RPM"
st = get("vcgencmd get_throttled").split('=')[1] or "0x0"

# Header & Rahmen
print(f"{Y}┏" + "━" * (W + 2) + f"┓{N}")
print(f"{Y}┃{N}{f'Pi5 System Status v{V}':^{W+2}}{Y}┃{N}")
print(f"{Y}┣" + "━" * (W + 2) + f"┫{N}")

# Reihen-Funktion (Absolut bündig)
def pr(l, v):
    line = f" {l:<12} : {v}"
    print(f"{Y}┃{N}{line:<{W+2}}{Y}┃{N}")

pr("Hardware", hw)
pr("Kernel", kn)
pr("CPU Temp", ct)
pr("NVMe Temp", nt)
pr("CPU Takt", cf)
pr("VCore", vc)
pr("Lüfter", fn)
pr("Status", st)

print(f"{Y}┣" + "━" * (W + 2) + f"┫{N}")

# Status-Zeile ohne Versatz
status_text = " System Nominal (Integrität OK)" if st in ["0x0", "0"] else " Anomalie detektiert!"
color = G if st in ["0x0", "0"] else '\033[0;31m'
# Hier liegt der Trick: Erst formatieren, dann Farbe einfügen
formatted_status = f"{status_text:<{W+2}}"
print(f"{Y}┃{N}{color}{formatted_status}{N}{Y}┃{N}")

print(f"{Y}┗" + "━" * (W + 2) + f"┛{N}")
print(f"Repo: {B}{REPO}{N}")
