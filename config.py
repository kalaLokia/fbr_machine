import configparser
import logging
import os

ROOT = "C:/fbr_machine/"
LOG_FILENAME = ROOT + 'logs.txt'

if not os.path.exists(ROOT):
    os.makedirs(ROOT)

logging.basicConfig(
    filename=LOG_FILENAME, 
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

config = configparser.ConfigParser(interpolation=None)
exists = config.read(ROOT + "config.ini")


TIENKANG_HOST=""
TIENKANG_PORT=""
TIENKANG_USER=""
TIENKANG_PASS=""
TIENKANG_FILE=""
SLACK_TOKEN=""
SLACK_CHANNEL=""


if exists:

    if config.has_section("FTP_TK"):
        try:
            TIENKANG_HOST = config["FTP_TK"]["TIENKANG_HOST"]
            TIENKANG_PORT = config["FTP_TK"]["TIENKANG_PORT"]
            TIENKANG_USER = config["FTP_TK"]["TIENKANG_USER"]
            TIENKANG_PASS = config["FTP_TK"]["TIENKANG_PASS"]
        except KeyError as e:
            logging.error("MADATORY KEYS NOT FOUND..!")

    if config.has_option("WEBHOOK", "SLACK_TOKEN"):
        value = config.get("WEBHOOK", "SLACK_TOKEN")
        if value.startswith("xoxb-"):
            SLACK_TOKEN = value

    if config.has_option("WEBHOOK", "SLACK_CHANNEL"):
        value = config.get("WEBHOOK", "SLACK_CHANNEL")
        if value.startswith("xoxb-"):
            SLACK_CHANNEL = value

    if config.has_option("WEBHOOK", "GOOGLE_WH"):
        value = config.get("WEBHOOK", "GOOGLE_WH")
        if value.startswith("https://chat.googleapis.com"):
            GOOGLE_WH = value


