"""
Indeed job notifier is a python script that automates job searching on
www.indeed.com and send notification email to the user when a new job 
matching the user's profile is posted.

It checks for new job posts every 3 days.

Author: @balewgize
Date: August, 2013 E.C
"""

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
        'authority': 'www.indeed.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.indeed.com/jobs?q=%22Python%20Developer%22&l=Remote&sort=date&fromage=3&start=10&vjk=8998cc80e1d0e19c',
        'accept-language': 'en-US,en;q=0.9',
    }

    response = requests.get('https://www.indeed.com/jobs', headers=headers, params=params)
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
    fieldnames = ['job_title', 'company_name', 'company_location', 'salary',
                'posted', 'extracted', 'job_summary', 'job_url']
    today = datetime.today().strftime('%Y-%m-%d')
    with open(f'job-list-{today}.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(job_list)

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


def main():
    response = basic_search()

    first_page = BeautifulSoup(response.content, 'lxml')
    all_jobs = extract_page(first_page)
    job_list = extract_next_pages(first_page)
    all_jobs.extend(job_list)

    save_to_csv(all_jobs)

if __name__ == '__main__':
    main() 