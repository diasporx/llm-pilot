import os
from dotenv import load_dotenv

load_dotenv()

TRACKER_TOKEN = os.environ["TRACKER_TOKEN"]
ORG_ID = os.environ["ORG_ID"]
ORG_TYPE = os.getenv("ORG_TYPE", "yandex360")
BASE_URL = os.getenv("BASE_URL", "https://api.tracker.yandex.net/v2")
