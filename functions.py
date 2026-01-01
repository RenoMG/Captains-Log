from astropy.time import Time
from datetime import date
import time

def thinking(seconds):
    time.sleep(seconds)
    print("Computer is thinking...")
    time.sleep(seconds)

def saving(seconds):
    time.sleep(seconds)
    print("Computer is saving data...")
    time.sleep(seconds)

def convert_date_to_julian():
    normal_date = date.today()
    return str(Time(str(normal_date)).jd)