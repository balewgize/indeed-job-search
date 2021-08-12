"""
Indeed job notifier is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's profile is posted.

It checks for new job posts every 3 days.

Author: @balewgize
Date: August, 2013 E.C
"""

import csv
import requests
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
    response = requests.get('https://www.indeed.com/jobs', params=params)
    return response


# def advanced_search():
#     """ Perform advanced job searching by filtering using different parameters."""
#     position = job_filter.get_position()
#     location = job_filter.get_location()
#     job_type = job_filter.get_job_type()
#     experience = job_filter.get_experience()

#     params = (
#         ('q', position),
#         ('l', location),
#         ('jt', job_type),
#         ('explvl', experience),
#     )
#     response = requests.get('https://www.indeed.com/jobs', params=params)
#     return response


def get_job_detail(card):
    """ Extract the Job details for a single job."""
    job_title = card.find('h2', 'jobTitle').contents[-1].text.strip()
    company_name = card.find('span', 'companyName').text.strip()
    company_location = card.find('div', 'companyLocation').contents[0].strip()
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
        'company_name': company_name,
        'company_location': company_location,
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


def save_to_csv(job_list):
    """ Write the list of jobs given to a csv file."""
    fieldnames = ['job_title', 'company_name', 'company_location', 'job_summary',
                'salary', 'posted', 'extracted', 'job_url']
    today = datetime.today().strftime('%Y-%m-%d')
    with open(f'job-list-{today}.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(job_list)



def main():
    response = basic_search()

    html = BeautifulSoup(response.content, 'lxml')
    job_list = extract_page(html)
    save_to_csv(job_list)

if __name__ == '__main__':
    main() 