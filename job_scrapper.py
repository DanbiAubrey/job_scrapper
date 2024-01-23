import requests
from bs4 import BeautifulSoup
from requests.models import LocationParseError

class Job():

  def __init__(self, title, link, location, salary):
    self.title = title
    self.company = link
    self.location = location
    self.salary = salary

class Scrapper():

  def __init__(self, url, keywords):
    self.url = url
    self.keywords = keywords
    self.all_jobs = []

  def scrape_page(self):
    
    for k in self.keywords:
      current_url = f"{self.url}/remote-{k}-jobs"
      r = requests.get(
          current_url,
          headers={
              "User-Agent":
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
          })
      soup = BeautifulSoup(r.content, "html.parser")
    
      print(f"Scrapping {current_url} ...")
    
      jobs = soup.find("table", id="jobsboard").find_all("tr", class_="job")
      for job in jobs:
        title = job.find("h2", itemprop="title").text
        locations = job.find_all("div", class_="location")
        link = job.find("td", class_="company").find("a", itemprop="url")["href"]
        link = f"https://remoteok.com/{link}"
        l_list = []
        for l in locations:
          l_list.append(l.text)
        location = l_list[0:-1]
        salary = l_list[-1]
        
        self.all_jobs.append(Job(title, link, location, salary))
    return self.all_jobs

url = f"https://remoteok.com"

keywords = ["flutter", "python", "golang"]

scrapper = Scrapper(url, keywords)
all_jobs = scrapper.scrape_page()
print(all_jobs)
print(f"number of all jobs: {len(all_jobs)}")