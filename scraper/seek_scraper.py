from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time
import requests

class Seek_Scraper:
    def __init__(self, keywords, region):
        self.url = f"https://www.seek.com.au/"
        self.keywords = keywords
        self.region = region
        self.jobs_db = []
    
    def playwright(self, keyword):
        p = sync_playwright().start() # initialize playwright object
        browser = p.chromium.launch(headless=False) # launch chrome browser instance / browser window visible mode
        page = browser.new_page() # create new browser page

        page.goto(self.url)
        time.sleep(3)
        page.locator('input#keywords-input').fill(f"{keyword}")
        time.sleep(3)
        page.keyboard.down("Enter")
        time.sleep(3)

        for i in range(3):
            page.keyboard.down("End")
            time.sleep(3)
        
        content = page.content()
        p.stop()

        page.screenshot(path="screenshot.png")

    def scraper(self):
        jobs_db = []
        #for keyword in self.keywords:
        for keyword in self.keywords:
            initial_url = f"{self.url}/{keyword}-jobs/in-All-{self.region}-QLD"
            r = requests.get(initial_url) # send get request to the url and return request.response object
            #last_page_num = get_last_page_num(current_url, keyword)
            last_page_num = self.get_last_page_num(initial_url, keyword)
            for i in range(1,last_page_num+1):
                current_url = f"{initial_url}/?page={i}"
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
                #print(jobs_db)
        return jobs_db

    def get_last_page_num(self, current_url, keyword):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(current_url)
            last_page = 1
            last_page_reached = False

            while not last_page_reached:
                try:
                    if page.query_selector("li.y735df0._1iz8dgsa6._1iz8dgs9v._1iz8dgsw"):
                        next_btn = page.query_selector("li.y735df0._1iz8dgsa6._1iz8dgs9v._1iz8dgsw").get_attribute('class')
                        class_name = str(next_btn).split(' ')
                        # print(class_name)
                        if len(class_name) == 4:
                            # print("clicked last button")
                            last_button = page.wait_for_selector("li.y735df0._1iz8dgs4u._1iz8dgs4z:not(._1iz8dgs8r)")
                            last_button.click()
                        else: # if there is no next button
                            # print("there is no next button")
                            last_page_reached = True
                            page_url = page.url
                            path_elements = page_url.split('=')
                            last_page = path_elements[-1]
                    else: # if there is no next button
                        # print("there is no next button")
                        last_page_reached = True
                        page_url = page.url
                        path_elements = page_url.split('=')
                        last_page = path_elements[-1]
                except Exception as e:
                    print(f"Error occured: {e}")
                    break
            browser.close()

        return int(last_page)
    
    def wrtie_csv(self, file_name, jobs_db):
        file  = open(f"{file_name}.csv", "w")
        writer = csv.writer(file)
        writer.writerow(jobs_db[0].keys())
        for job in jobs_db:
            writer.writerow(job.values()) 
        file.close()

    def execute(self):
        print("start scraping jobs from seek..")
        jobs_db = self.scraper()
        print("start writing csv file...")
        self.wrtie_csv("jobs", jobs_db)

