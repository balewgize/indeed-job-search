"""
Indeed job notifier is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's profile is posted.

It checks for new job posts every 3 days.

Author: @balewgize
Date: August, 2013 E.C
"""

import os
import csv
import time
import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup

import job_filter


def search_jobs(preferences):
    """ Search jobs based on user preference."""
    url = 'https://www.indeed.com/jobs'
    headers = {
        'user-agent': 'Mozilla/5.0',
    }
    response = requests.get(url, headers=headers, params=preferences)
    return response


def get_job_detail(card):
    """ Extract the Job details for a single job."""
    title_con = card.find('h2', 'jobTitle').contents[-1]
    job_title = title_con.text.strip()

    company_con = card.find('span', 'companyName')
    company = company_con.text.strip()

    location_con = card.find('div', 'companyLocation')
    location = location_con.contents[0].strip()

    posted = card.find('span', 'date').text.strip()
    today = datetime.today().strftime("%Y-%m-%d")

    job_summary = card.find('div', 'job-snippet').text.strip()
    job_url = f"https://www.indeed.com{card.get('href')}"

    try:
        salary = card.find('span', 'salary-snippet').text.strip()
    except AttributeError:
        salary = 'N/A'

    job = {
        'job_title': job_title,
        'company': company,
        'location': location,
        'salary': salary,
        'posted': posted,
        'extracted': today,
        'job_summary': job_summary,
        'job_url': job_url
    }
    return job


def extract_page(html):
    """ Extract details for all jobs on a single page."""
    cards = html.find_all('a', 'tapItem')
    job_list = []
    for card in cards:
        job = get_job_detail(card)
        job_list.append(job)

    return job_list

def extract_next_pages(current_page):
    """ Extract next result pages from the current page."""
    job_list = []

    while True:
        next_page = current_page.find('a', {'aria-label': 'Next'})
        try:
            next_url = f"https://www.indeed.com{next_page.get('href')}"
        except AttributeError:
            # we reach the end of all job posts (no next button)
            break

        response = requests.get(next_url)
        current_page = BeautifulSoup(response.content, 'lxml')
        jobs = extract_page(current_page)
        job_list.extend(jobs)

        time.sleep(random.randint(6, 10))

    return job_list


def save_to_csv(job_list):
    """ Write the list of jobs given to a csv file."""
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f'Desktop/job-list-{today}.csv'
    full_path = os.path.join(get_home_dir(), filename)

    with open(full_path, 'w') as file:
        fieldnames = job_list[0].keys()
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(job_list)

    print("The result has been saved to a csv file on your Desktop.")


def get_user_preferences():
    """ Get the user preference to save for later use."""
    positions = job_filter.get_positions()
    locations = job_filter.get_locations()
    job_types = job_filter.get_job_types() 
    experiences = job_filter.get_experiences()

    save_user_preferences(positions, locations, job_types, experiences)


def get_home_dir():
    """ Get the home directory of the user."""
    if os.name == 'nt':  
        # windows OS
        home_dir = 'C:' + os.getenv('HOMEPATH')
    else:  
        # Unix-like OS
        home_dir = os.getenv('HOME')

    return home_dir


def read_user_preferences():
    """ Read preferences of the user if it has been saved."""
    home_dir = get_home_dir()
    full_path = os.path.join(home_dir, '.job-preferences.txt')

    with open(full_path) as file:
        lines = file.readlines()
        lines = list(map(lambda x: x.replace('\n', ''), lines))
        positions = lines[0].split(',')
        locations = lines[1].split(',')
        job_types = lines[2].split(',')
        experiences = lines[3].split(',')

    sort_by = 'date'
    last_three_days = '3'

    # how to handle all variation of this preferences?

    params = (
        ('q', positions[0]),
        ('l', locations[0]),
        ('jt', job_types[0]),
        ('explvl', experiences[0]),
        ('sort', sort_by),
        ('fromage', last_three_days),
    )
    return params


def save_user_preferences(positions, locations, job_types, experiences):
    """ Save user preferences for later use."""
    def convert_to_str(iterable):
        """ Conver an iterable to comma separated string."""
        line = ''
        for item in iterable:
            line += item + ','
        return line[:-1]

    filename = '.job-preferences.txt'
    home_dir = get_home_dir()
    full_path = os.path.join(home_dir, filename)
    
    with open(full_path, 'w') as file:
        file.write(convert_to_str(positions)+'\n')
        file.write(convert_to_str(locations)+'\n')
        file.write(convert_to_str(job_types)+'\n')
        file.write(convert_to_str(experiences)+'\n')


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

    # check if the user have set preferences
    home_dir = get_home_dir()
    filename = '.job-preferences.txt'
    full_path = os.path.join(home_dir, filename)

    if os.path.exists(full_path):
        # the user has set preference, so read and use that
        preferences = read_user_preferences()

        # make job search based on user preferences
        print("\nSearching for jobs...")
        response = search_jobs(preferences)

        first_page = BeautifulSoup(response.content, 'lxml')
        all_jobs = extract_page(first_page)
        job_list = extract_next_pages(first_page)
        all_jobs.extend(job_list)

        # now look jobs retrived and send an email

        save_to_csv(all_jobs)

    else:
        welcome()

        ch = input('Would you like to set/update your preference now? [Y/N]: ')
        if ch.lower() == 'y' or ch.lower() == 'yes':
            get_user_preferences()
            clear_screen()
            print('\nYour job preferences has been saved.')
            print('You can now run the script again to search for jobs matching your preferences.')
        else:
            print('Thank you!.')


if __name__ == '__main__':
    main() 