"""
Indeed job search is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's profile is posted.

It checks for new job posts every 3 days.

Author: @balewgize
Date: August, 2013 E.C
"""
from bs4 import BeautifulSoup

from email_sender import EmailSender
from user_preference import Profile
from job_scraper import IndeedJobScraper


def send_email(to, params, total):
    """ Send email notification about the jobs posted."""
    import requests
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    base_url = 'https://www.indeed.com/jobs'
    job_url = requests.get(base_url, params=params).url

    subject = f'New Indeed jobs for you on {today}'

    text = f"""\
        Hello Alemnew,

        {total} New jobs matching your preference have been posted in the last three days

        See details and Apply here: {job_url}

        Good Luck,
        Python Email Sender
    """

    html = f"""\
        <html>
        <body>
            <p> Hello Alemnew, <br> <br>
                {total} New jobs matching your preference have been posted in the last three days.
                <br><br>
                Take a look here: <br> {job_url}
            </p>
            <p>
                Good Luck, <br>
                Python Email Sender
            </p>
        </body>
        </html>
    """
    email_sender = EmailSender()
    email_sender.send(to, subject, text, html)


def save_to_excel(data):
    """ Save job search results to an excel file."""
    import os
    import pandas as pd
    from datetime import datetime

    today = datetime.today().strftime('%Y-%m-%d')
    desktop = os.path.expanduser('~/Desktop/')
    filename = f'job-list-{today}.xlsx'
    full_path = os.path.join(desktop, filename)

    df = pd.DataFrame(data)
    df.to_excel(full_path, sheet_name=f'Jobs-{today}', index=False)


def save_to_csv(job_list):
    """ Write the list of jobs given to a csv file."""
    import os, csv
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


def welcome():
    """ Show welcome message."""
    msg = 'Indeed Job Search'
    print(f"{'-'*50}\n{'Welcome!':^50}\n{msg:^50}\n{'-'*50}")
    print("""
    I use your job preference to search for jobs
    relevant to you.

    When I found relevant jobs, I immediately
    send you an email notification so you can 
    apply before a deadline.

    Lastly, I will search for jobs every
    three days. No need of always checking 
    the website. 

    Now job searching on indeed.com is automated.
    """)
    print('-'*50, '\n')


def main():
    clear_screen()
    welcome()

    profile = Profile()
    scraper = IndeedJobScraper()

    preference = profile.read_user_preferences()
    print("\nSearching for jobs...")
    response = scraper.search_jobs(preference)

    first_page = BeautifulSoup(response.content, 'lxml')
    data = scraper.extract_all_pages(first_page)

    to = 'alemnewmarie461@gmail.com'
    send_email(to, preference, len(data['Job Title']))

    save_to_excel(data)
    # save_to_csv(all_jobs)


if __name__ == '__main__':
    main() 