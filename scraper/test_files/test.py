from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time
import requests

url = f'https://www.seek.com.au/'
keywords = ['Web-Developer', 'data scientist', 'machine learning']
region = 'Brisbane'

current_url = f'{url}/{keywords[0]}-jobs/in-{region}'
r = requests.get(current_url)
soup = BeautifulSoup(r.content, 'html.parser')

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto(current_url)
#     last_page = 1
#     last_page_reached = False

#     while not last_page_reached:
#         try:
#             last_button = page.wait_for_selector('li.y735df0._1iz8dgs4u._1iz8dgs4z:not(._1iz8dgs8r)')
#             last_button.click()
#             if not page.query_selector('li.y735df0._1iz8dgsa6._1iz8dgs9v._1iz8dgsw'): # if there is no next button
#                 last_page_reached = True
#                 page_url = page.url
#                 path_elements = page_url.split('=')
#                 print(path_elements)
#                 last_page = path_elements[-1]
                
#                 print(last_page)
#         except Exception as e:
#             print(f'Error occured: {e}')
#             break
#     browser.close()


for keyword in keywords:
    current_url = f'{url}/{keyword}-jobs/in-All-{region}-QLD'
    r = requests.get(current_url) # send get request to the url and return request.response object
    
    for i in range(1,14):
        r = requests.get(current_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        jobs = soup.find_all('div', class_='y735df0 _1iz8dgs9y _1iz8dgs9r _1iz8dgs8u _1iz8dgs8n')
        jobs = [div for div in jobs if len(div.get('class', [])) == 5][3]
        jobs = jobs.find_all('div', class_='y735df0 _1iz8dgs6m')
        print(len(jobs))
        jobs = [div for div in jobs if len(div.get('class', [])) == 2]
        print(current_url)
        print(len(jobs))
        #print(jobs)

        for job in jobs:
            title = job.find('div', class_='y735df0 _1iz8dgs6m')
            title = [div for div in title if len(div.get('class', [])) == 2]
            title = title.find('div', class_="y735df0")
            print(len(title))
            #print(title)
            exit()
            #.find('a')['href'].text
            link = f"https://www.seek.com.au/{job.find('div', class_='y735df0 _1iz8dgs4y _1iz8dgs4w').find('a')['href']}"
            job_type = job.find('div', class_='y735df0 _1iz8dgs5i _1iz8dgs0 _14zgbb20').find('p', class_='y735df0').text
            job_type = job_type.replace('This is a ', '').replace(' job', '')
            location  = f"{job.find('span', class_='y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w21 _1wzghjf4 _94v4w7').find('span', class_='y735df0').find('a')['href'].text}"
            spec = job.find('div', class_='y735df0 _1iz8dgs6m _1iz8dgs4u _1iz8dgs4z').find('div', class_='y735df0 _1iz8dgsr _1iz8dgsf6 _1iz8dgsbu _1iz8dgs4y _1iz8dgsfm').find('a')['href']

       
       
            #print(title, link, job_type, location, spec)
        file_name = "file"
        file  = open(f"{file_name}.csv", "w")
        writer = csv.writer(file)
        writer.writerow(jobs.keys())
        for job in jobs:
            writer.writerow(job.values())