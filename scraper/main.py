import argparse
import time
from seek_scraper import Seek_Scraper 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrapes jobs from https://www.seek.com.au/")
    parser.add_argument('--keywords', nargs='+', type=str, help='list of jobs')
    parser.add_argument('--region', type=str, default='brisbane', help='Location of jobs')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()

    keywords = args.keywords
    region = args.region

    s = time.time()
    scraper = Seek_Scraper(keywords, region)
    scraper.execute()
    e = time.time()

    print("Running Time: %f s" % (e - s))