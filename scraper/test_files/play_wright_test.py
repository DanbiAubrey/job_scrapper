from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time
import requests

p = sync_playwright().start() # initialize playwright object
browser = p.chromium.launch(headless=False) # launch chrome browser instance / browser window visible mode
page = browser.new_page() # create new browser page

page.goto("https://www.seek.com.au/")
time.sleep(3)
page.locator('input#keywords-input').fill("Web-Developer")
time.sleep(3)
page.keyboard.down("Enter")
time.sleep(3)

for i in range(3):
    page.keyboard.down("End")
    time.sleep(3)

content = page.content()
p.stop()

page.screenshot(path="screenshot.png")