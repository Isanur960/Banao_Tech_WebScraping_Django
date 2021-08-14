from requests import status_codes
from w3lib.html import get_base_url
import extruct
from pprint import pprint
import requests
from bs4 import BeautifulSoup


def get_html(url):
    print(url)
    req = requests.get(url)
    return req.text


def scrape(url):
    html = get_html(url)
    metadata = get_metadata(html, url)
    # pprint(metadata, indent=2, width=150)
    return metadata


def get_metadata(html: bytes, url: str):
    metadata = extruct.extract(
        html,
        base_url=get_base_url(url),
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']
    return metadata


# x = scrape("https://www.talentrack.in/jobdetail/looking-for-professional-singers-for-our-production-house_152869?tag=")
# scrape("https://www.iimjobs.com/j/sales-manager-marine-business-software-5-15-yrs-961693.html?ref=sp")

# scrape("https://internshala.com/fresher-job/detail/executive-senior-executive-partnerships-fresher-jobs-in-multiple-locations-at-freecharge-payments-technology-private-limited1628770904")

# print(x['title'])


def internshala():
    url = "https://internshala.com/fresher-jobs/"
    base_url = "https://internshala.com"
    res = requests.get(url)
    print(res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    all_job = soup.find_all(class_="internship_meta")
    all_link = [x['href'] for x in soup.find_all("a", href=True)]
    # print(len(all_link))
    # print(len(all_job))
    for job in all_job:
        job_soup = BeautifulSoup(str(job), 'html.parser')
        job_name_soup = job_soup.find(class_="heading_4_5 profile")
        job_link_soup = BeautifulSoup(str(job_name_soup), 'html.parser')
        job_link = job_link_soup.find("a", href=True)['href']
        while True:
            if job_link in all_link:
                d = all_link.index(job_link)
                print(d)
                all_link.pop(d)
            else:
                break
        interesting_url = base_url + job_link
        print(interesting_url)
        # details = scrape(interesting_url)[-1]
        # print(details['title'])
        break


def iimjobs():
    url = "https://www.iimjobs.com/search/developer-0-0-0-1.html"
    base_url = "iimjobs.com/"
    res = requests.get(url)
    print(res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    all_job = soup.find_all(
        class_="mrmob5 hidden-xs")
    all_link = [x['href'] for x in soup.find_all("a", href=True)]
    # print(len(all_link))
    # print(len(all_job))
    for job in all_job:
        job_soup = BeautifulSoup(str(job), 'html.parser')
        job_link = job_soup.find("a", href=True)['href']
        while True:
            if job_link in all_link:
                d = all_link.index(job_link)
                print(d)
                all_link.pop(d)
            else:
                break
        interesting_url = job_link
        print(interesting_url)
        # details = scrape(interesting_url)[0]
        # print(details['title'])
        break


def talentrack():
    url = "https://www.talentrack.in/all-job-in-india"
    base_url = "https://www.talentrack.in"
    res = requests.get(url)
    print(res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    all_job = soup.find_all(
        class_="job-listing-new")
    all_link = [ x['href'] for x in soup.find_all("a", href=True)]
    # print(len(all_link))
    # print(len(all_job))
    for job in all_job:
        job_soup = BeautifulSoup(str(job), 'html.parser')
        job_link = job_soup.find("a", href=True)['href']
        while True:
            if job_link in all_link:
                d = all_link.index(job_link)
                print(d)
                all_link.pop(d)
            else:
                break
        interesting_url = base_url + job_link
        print(interesting_url)
        # details = scrape(interesting_url)[0]
        # print(details['title'])
        break


internshala()
iimjobs()
talentrack()
# scrape("www.iimjobs.com/j/sales-manager-marine-business-software-5-15-yrs-961693.html?ref=sp")
