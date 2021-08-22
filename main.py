"""
Indeed job search is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's preference is posted.

It automatically checks for new job posts every Tuesday and Friday at 
06:00 AM if the device is connected to the internet.

Author: @balewgize
Date: August, 2013 E.C
"""
import os, time, random
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

from email_sender import EmailSender
from user_preference import Profile
from job_scraper import IndeedJobScraper


def send_email(to, params, jobs_url):
    """ Send email notification about the jobs posted."""
    today = datetime.today().strftime('%Y-%m-%d')
    subject = f'New Indeed jobs for you on {today}'

    text = "Hello Alemnew,\n\n" + \
            "New jobs posts in the last three days.\n\n"
    for param, url in zip(params, jobs_url):
        position = param[0][1][1:-1]
        location = param[1][1]
        count = count_jobs(position, location)
        if count > 0:
            text += f'{count} {position} jobs in {location}\n'
    text += "\nGood Luck!"

    html = f"""\
    <html>
    <body>
        <p> Hello Alemnew, <br> <br>
            New job posts in the last three days. <br><br>
        </p>
    """
    for param, url in zip(params, jobs_url):
        position = param[0][1][1:-1]
        location = param[1][1]
        count = count_jobs(position, location)
        if count > 0:
            html += f'<a href="{url}">{count} {position} jobs in {location}</a> <br>'

    html += """
        <p>
            Good Luck, <br>
            Python Email Sender
        </p>
    </body>
    </html>
    """
    email_sender = EmailSender()
    email_sender.send(to, subject, text, html)

def count_jobs(position, location):
    """ Return how many jobs with the given postion and location."""
    today = datetime.today().strftime('%Y-%m-%d')
    home_dir = get_home_dir()
    filename = f'job-list-{today}.xlsx'
    full_path = os.path.join(home_dir, 'Desktop/'+filename)

    jobs = pd.read_excel(full_path)
    filter = (jobs['Position'] == position) & \
            (jobs['Location'] == location)
    filtered_jobs = jobs.loc[filter]
    count = len(filtered_jobs)

    if count == 0:
        filter = (jobs['Position'] == position)
        filtered_jobs = jobs.loc[filter]
        count = len(filtered_jobs)

    return count

def save_to_excel(data):
    """ Save job search results to an excel file."""
    import pandas as pd

    today = datetime.today().strftime('%Y-%m-%d')
    home_dir = get_home_dir()
    filename = f'job-list-{today}.xlsx'
    full_path = os.path.join(home_dir, 'Desktop/'+filename)

    df = pd.DataFrame(data)
    df.to_excel(full_path, sheet_name=f'Jobs-{today}', index=False)


def get_home_dir():
    """ Get the home directory of the user based the Operating System."""
    import os
    if os.name == 'nt': 
        return os.path.expanduser('~\\')
    else:
        return os.path.expanduser('~/')

def clear_screen():
    """ Clears the stdout screen."""
    import os
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    clear_screen()

    profile = Profile()
    scraper = IndeedJobScraper()

    jobs_url = [] # url to the result page of each job search

    preference = profile.read_user_preferences()
    print("\nSearching for jobs...")
    for params in preference:
        params = list(params)
        params.append(('sort', 'date')) # newest first
        params.append(('fromage', '3')) # last three days
        params = tuple(params)
        position = params[0][1][1:-1] # e.g Python developer

        response = scraper.search_jobs(params)
        jobs_url.append(response.url)

        if response.status_code == 200:
            first_page = BeautifulSoup(response.content, 'lxml')
            scraper.extract_all_pages(first_page, position)
        # wait some seconds before sending the next request    
        time.sleep(random.randint(6, 10))

    data = scraper.data
    save_to_excel(data)

    # TO: this email address is used by the scipt to send you notificaion emails when new job
    # posts matching your prefernce is posted
    
    to = 'Your second Email address here'
    send_email(to, preference, jobs_url)