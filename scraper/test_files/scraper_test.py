from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time
import requests

url = f"https://www.seek.com.au/"
keywords = ["Web-Developer", "data scientist", "machine learning"]
region = "Brisbane"

def get_last_page_num(current_url, keyword):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(current_url)
            last_page = 1
            last_page_reached = False

            while not last_page_reached:
                try:
                    last_button = page.wait_for_selector("li.y735df0._1iz8dgs4u._1iz8dgs4z:not(._1iz8dgs8r)")
                    last_button.click()
                    if not page.query_selector("li.y735df0._1iz8dgsa6._1iz8dgs9v._1iz8dgsw"): # if there is no next button
                        last_page_reached = True
                        page_url = page.url
                        path_elements = page_url.split('=')
                        last_page = path_elements[-1]
                except Exception as e:
                    print(f"Error occured: {e}")
                    break
            browser.close()

        return last_page

for keyword in keywords:
    initial_url = f"{url}/{keyword}-jobs/in-All-{region}-QLD"
    r = requests.get(initial_url) # send get request to the url and return request.response object
    #last_page_num = get_last_page_num(current_url, keyword)
    last_page_num = 10
    jobs_db = []
    for i in range(1,last_page_num+1):
        current_url = f"{initial_url}/?page={i}"
        print(current_url)
        r = requests.get(current_url)
        soup = BeautifulSoup(r.content, "html.parser")
        #articles = soup.select('article[data-testid="job-card"]')
        articles = soup.find_all('article', attrs={'data-testid': 'job-card'})
        jobs = []
        
        for article in articles:
            job_card = article.select_one('div.y735df0._1akoxc50._1akoxc56')
            jobs.append(job_card)
        
        for job in jobs:
            title = job.find('h3').find('a').text
            company_name = job.find('h3').find('a').find_next('a').text
            link = f"https://www.seek.com.au/{job.find('div', class_='y735df0 _1iz8dgs5g _1iz8dgs52').find('a')['href']}"
            job_type = job.find('div', class_='y735df0 _1iz8dgs5i _1iz8dgs0 _14zgbb20').find('p', class_="y735df0").text
            job_type = job_type.replace("This is a ", "").replace(' job', "")
            span = job.find('span', class_="y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w21 _4rkdcp4 _94v4w7")
            spans = span.find_all('span', class_='y735df0')
            filtered_span = [span for span in spans if len(span['class']) == 1]
            location  = f"{filtered_span[0].find('a').text}"
            job_db = {
                'title' : title,
                'company_name' : company_name,
                'link' : link,
                'job type' : job_type,
                'location' : location
            }

            jobs_db.append(job_db)

        file_name = "file"
        file  = open(f"{file_name}.csv", "w")
        writer = csv.writer(file)
        writer.writerow(jobs_db[0].keys())
        for job in jobs_db:
            writer.writerow(job.values())   

        
        # current_url = f"{url}/{keyword}-jobs/in-All-{region}-QLD?page={i}"