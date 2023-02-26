import logging
import sys
import time
from logging.handlers import RotatingFileHandler

import requests
import sentry_sdk
from tinydb import TinyDB, where

from porte import CONFIG, HID, UnknownDevice

ADMIN_CHOUETTOS_URL = "https://adminchouettos.lachouettecoop.fr/api/export/gh"
CHANNEL_NB = 21
DB = TinyDB("synchro-gh.json")
SCANNETTES = [
    "0003:0C2E:0200",
    "0003:05E0:1200",
]

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
s_handler = logging.StreamHandler()
s_handler.setFormatter(formatter)
logger.addHandler(s_handler)
f_handler = RotatingFileHandler(
    filename="porte.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
    encoding="utf-8",
)
f_handler.setFormatter(formatter)
logger.addHandler(f_handler)

sentry_config = CONFIG.get("sentry")
if sentry_config:
    sentry_sdk.init(dsn=sentry_config.dsn, traces_sample_rate=1.0)


def print_device_id(d):
    logging.info(d.device_path)


def check_device(d):
    for part in d.device_path.split("/"):
        for s in SCANNETTES:
            if part.startswith(s):
                return True
    return False


def is_gh(code_barre):
    if code_barre in CONFIG.get("default_gh_list", []):
        logging.info(f"{code_barre} is in default list")
        return True
    gh = DB.get(where("code_barre") == code_barre)
    if gh:
        logging.info(f"{code_barre} is a GH")
        return True
    logging.warning(f"{code_barre} is not a GH")
    return False


# http://www.piddlerintheroot.com/5v-relay/
# https://www.piddlerintheroot.com/barcode-scanner/
def scanette():
    import pyudev as pd
    import RPi.GPIO as GPIO

    # La scanette ne se mettait pas toujours sur le /dev/hidraw0 (parfois hidraw1, 2 etc...)
    # ce petit script permet de determiner le bon hidraw dynamiquement !
    # @thone https://www.instructables.com/id/USB-Barcode-Scanner-Raspberry-Pi/
    context = pd.Context()
    location = None
    for device in context.list_devices(subsystem="hidraw"):
        # print_device_id(device)
        if check_device(device):
            location = device.device_node

    logging.info("--- Démarrage du serveur de porte ---")
    if not location:
        logging.error("Scannette introuvable !")
        raise UnknownDevice(context)

    try:
        # attention le CHANNEL_NB peut changer a certains moments
        fp = open(location, "rb")
        while True:
            v = ""
            done = False
            while not done:
                buffer = fp.read(8)
                for c in buffer:
                    if int(c) == 40:
                        done = True
                        break
                    if int(c) > 28:
                        if int(HID[int(c)]) >= 0:
                            v = v + HID[int(c)]

            if is_gh(v):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(CHANNEL_NB, GPIO.OUT)
                logging.info("Nouvelle ouverture " + str(v))
                GPIO.output(CHANNEL_NB, GPIO.HIGH)  # Turn motor on
                time.sleep(1)
                GPIO.output(CHANNEL_NB, GPIO.LOW)  # Turn motor off
                time.sleep(1)
                GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()


def refresh():
    r = requests.get(ADMIN_CHOUETTOS_URL)

    if r.status_code == 200:
        DB.drop_tables()
        for code_barre in r.json():
            DB.insert({"code_barre": code_barre})
        logging.info("La liste des GH est à jour")
    else:
        logging.error(f"Erreur {r.status_code}: {r.text}")


if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] == "scan":
        scanette()
    elif sys.argv[1] == "refresh":
        refresh()
