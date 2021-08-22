"""
Schedule to search jobs every Tuesday and Friday at 6:00 AM
"""

import time
import schedule

import main


def is_connected():
    """ Check if a device is connected to the internet or not."""
    import requests
    try:
        headers = {
            'user-agent': 'Mozilla/5.0'
        }
        requests.get('https://www.indeed.com', headers=headers, timeout=10)
        return True

    except (requests.ConnectionError, requests.ConnectTimeout):
        return False


def search_jobs():
    """ Triggers the main function of main.py"""
    connected = is_connected()
    if connected:
        main.main() # search jobs and send an email
        # once the job search is done, cancel the job task
        return schedule.CancelJob

""" Since the device may not be always connected to the internet at 06:00 AM,
    we need to check whether the device has an internet connection every 30 min
"""

schedule.every(10).minutes.do(search_jobs)

while True:
    n = schedule.idle_seconds()
    if n is None:
        break # no more jobs
    elif n > 0:
        time.sleep(n) # sleep the right amount of time
        
    schedule.run_pending()