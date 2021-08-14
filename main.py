"""
Indeed job notifier is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's profile is posted.

It checks for new job posts every 3 days.

Author: @balewgize
Date: August, 2013 E.C
"""

import os, csv
from bs4 import BeautifulSoup

from email_sender import EmailSender
from user_preferences import Profile
from job_scraper import IndeedJobScraper


def save_to_excel(job_list):
    """ Save job search results to an excel file."""
    pass


def save_to_csv(job_list):
    """ Write the list of jobs given to a csv file."""
    from datetime import datetime

    today = datetime.today().strftime('%Y-%m-%d')
    desktop = os.path.expanduser('~/Desktop/')
    filename = f'job-list-{today}.csv'
    full_path = os.path.join(desktop, filename)

    with open(full_path, 'w') as file:
        fieldnames = job_list[0].keys()
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(job_list)

    print("The result has been saved to a csv file on your Desktop.")


def get_home_dir():
    """ Get the home directory of the user based the Operating System."""
    if os.name == 'nt': 
        return os.path.expanduser('~\\')
    else:
        return os.path.expanduser('~/')

def clear_screen():
    """ Clears the stdout screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def welcome():
    """ Show welcome message."""
    msg = 'Indeed Job Post Notifier'
    print(f"{'-'*50}\n{'Welcome!':^50}\n{msg:^50}\n{'-'*50}")
    print("""
    It is your first time using the app,
    please tell me your job preferences so that
    I can automate job searching on indeed.com

    If I found jobs relevant to you, I will
    send you an email immediately so you can 
    apply before a deadline.

    Besides that I will check indeed.com every
    three days and tell you report of jobs
    posted during those days. 
    """)
    print('-'*50, '\n')


def main():
    clear_screen()

    profile = Profile()
    email_sender = EmailSender()
    scraper = IndeedJobScraper()

    preferences = profile.read_user_preferences()
    print("\nSearching for jobs...")
    response = scraper.search_jobs(preferences)

    first_page = BeautifulSoup(response.content, 'lxml')
    all_jobs = scraper.extract_page(first_page)
    job_list = scraper.extract_next_pages(first_page)
    all_jobs.extend(job_list)

    # now look jobs retrived and send an email
    save_to_excel(all_jobs)
    save_to_csv(all_jobs)


if __name__ == '__main__':
    main() 