#!/usr/bin/env python3

import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint


def get_url(location):
        template = 'https://au.indeed.com/jobs?l={}'
        url = template.format(location)
        return url


def get_job(card):
    '''Extract job date from a single record '''
    job = {}

    try:
        if card.find('h2', 'jobTitle').next_sibling is not None:
            job['job_title'] = card.find('h2', 'jobTitle').span.text.strip()
        else: 
            job['job_title'] = card.find('h2', 'jobTitle').text.strip()
        job['company'] = card.find('span', 'companyName').text.strip()
        job['company_location'] = card.find('div', 'companyLocation').text.strip()
    except Exception as e:
        raise Exception(str(e))
    
    job['extract_date'] = datetime.today().strftime('%Y-%m-%d')
    #job['job_url'] = 'https://www.indeed.com' + card.get('href')
    
    return job

def main():
    # Run the main program reouting
    print('here')
    jobs = []  # creating the record list
    url = get_url('Australia')  # create the url while passing in the position and location.
    
    while True:
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all("div", "job_seen_beacon")

        #print(cards)
        for card in cards:
            job = get_job(card)
            jobs.append(job)

        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            delay = randint(1, 10)
            sleep(delay)
        except AttributeError:
            break

    with open(f'IndeedJobs.json', 'w', encoding='utf8', newline='') as output_file:
        json.dump(jobs, output_file, indent=4)

if __name__ == "__main__":
    main()