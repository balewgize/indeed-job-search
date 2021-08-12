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


def basic_search():
    """ Perform basic job search based on postion and location."""
    # position = job_filter.get_position()
    # location = job_filter.get_location()
    position = '"Python Developer"'
    location = 'Remote'
    sort_by = 'date'
    last_three_days = '3'

    params = (
        ('q', position),
        ('l', location),
        ('sort', sort_by),
        ('fromage', last_three_days),
    )

    headers = {
        'user-agent': 'Mozilla/5.0',
    }

    response = requests.get('https://www.indeed.com/jobs', headers=headers, params=params)
    return response


def advanced_search():
    """ Filter the jobs to match the user preference."""
    position = '"Python Developer"'
    location = 'Remote'
    job_type = 'fulltime' # fulltime, contract, parttime
    experience = 'entry_level' # entry_level, mid_level, senior_level

    sort_by = 'date'
    last_three_days = '3'

    params = (
        ('q', position),
        ('l', location),
        ('jt', job_type),
        ('explvl', experience),
        ('sort', sort_by),
        ('fromage', last_three_days),
    )

    headers = {
        'user-agent': 'Mozilla/5.0',
    }

    response = requests.get('https://www.indeed.com/jobs', headers=headers, params=params)
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
    fieldnames = job_list[0].keys()
    today = datetime.today().strftime('%Y-%m-%d')
    with open(f'job-list-{today}.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(job_list)

def get_user_preference():
    """ Get the user preference and save for later use."""
    positions = job_filter.get_positions()
    locations = job_filter.get_locations()
    job_types = job_filter.get_job_types() 
    experiences = job_filter.get_experiences() 

    sort_by = 'date'
    last_three_days = '3'

    params = (
        ('q', positions[0]),
        ('l', locations[0]),
        ('jt', job_types[0]),
        ('explvl', experiences[0]),
        ('sort', sort_by),
        ('fromage', last_three_days),
    )


def welcome():
    """ Show welcome message."""
    msg = 'Indeed Job Post Notifier'
    print(f"'-'*50\n{'Welcome!':^50}\n{msg:^50}\n{'-'*50}")
    print("""
    If it is your first time using the app,
    let's see what it does assuming your are
    searching for postion "Python Developer"
    and you want to work "remotely".

    If it finds jobs relevant to you, it will
    send an email so that you can apply before
    a deadline.

    So to get email notificaions and automate
    job searching on indeed, please tell me 
    your preference so that I can check up new
    job posts every three days and send an email
    when I found relevant jobs for you.
    """)
    print('-'*50, '\n')


def main():
    welcome()

    ch = input('Would you like to update your preference now? [Y/N]: ')
    if ch.lower() == 'y' or ch.lower() == 'yes':
        get_user_preference()

    else:
        print('Thank you!.')

    response = basic_search()

    first_page = BeautifulSoup(response.content, 'lxml')
    all_jobs = extract_page(first_page)
    job_list = extract_next_pages(first_page)
    all_jobs.extend(job_list)

    save_to_csv(all_jobs)

if __name__ == '__main__':
    main() 