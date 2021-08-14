from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import pandas as pd
import os
from requests import status_codes
from w3lib.html import get_base_url
import extruct
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from .models import interesting_url, non_interesting_url, Categories, JobDB


def dlt():
    JobDB.objects.all().delete()
    Categories.objects.all().delete()
    interesting_url.objects.all().delete()
    non_interesting_url.objects.all().delete()


def get_html(url):
    # print(url)
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


def internshala():
    url = "https://internshala.com/fresher-jobs/"
    base_url = "https://internshala.com"
    res = requests.get(url)
    # print(res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    all_job = soup.find_all(class_="internship_meta")
    all_link = [x['href'] for x in soup.find_all("a", href=True)]
    # print(len(all_link))
    # print(len(all_job))
    n = 0
    for job in all_job:
        job_soup = BeautifulSoup(str(job), 'html.parser')
        job_name_soup = job_soup.find(class_="heading_4_5 profile")
        job_link_soup = BeautifulSoup(str(job_name_soup), 'html.parser')
        job_link = job_link_soup.find("a", href=True)['href']
        while True:
            if job_link in all_link:
                d = all_link.index(job_link)
                # print(d)
                all_link.pop(d)
            else:
                break
        interesting_urll = base_url + job_link
        il = interesting_url(url=interesting_urll)
        il.save()
        print("Saved(interesting url) :> ", interesting_urll)
        n = n + 1
        if n == 10:
            break
        # print(interesting_urll)
        # details = scrape(interesting_url)[-1]
        # print(details['title'])

    for el in all_link:
        if el[0] == '/':
            el = base_url + el
        il = non_interesting_url(url=el)
        il.save()
        print("Saved(Non interesting url) :> ", el)
        


def iimjobs():
    url = "https://www.iimjobs.com/search/developer-0-0-0-1.html"
    base_url = "iimjobs.com/"
    res = requests.get(url)
    # print(res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    all_job = soup.find_all(
        class_="mrmob5 hidden-xs")
    all_link = [x['href'] for x in soup.find_all("a", href=True)]
    # print(len(all_link))
    # print(len(all_job))
    n = 0
    for job in all_job:
        job_soup = BeautifulSoup(str(job), 'html.parser')
        job_link = job_soup.find("a", href=True)['href']
        while True:
            if job_link in all_link:
                d = all_link.index(job_link)
                # print(d)
                all_link.pop(d)
            else:
                break
        interesting_urll = job_link
        il = interesting_url(url=interesting_urll)
        il.save()
        print("Saved(interesting url) :> ", interesting_urll)
        n = n +1
        if n == 10:
            break
        # print(interesting_urll)
        # details = scrape(interesting_url)[0]
        # print(details['title'])

    for el in all_link:
        if el[0] == '/':
            el = base_url + el
        il = non_interesting_url(url=el)
        il.save()
        print("Saved(Non interesting url) :> ", el)


def talentrack():
    url = "https://www.talentrack.in/all-job-in-india"
    base_url = "https://www.talentrack.in"
    res = requests.get(url)
    # print(res.status_code)
    soup = BeautifulSoup(res.content, 'html.parser')
    all_job = soup.find_all(
        class_="job-listing-new")
    all_link = [x['href'] for x in soup.find_all("a", href=True)]
    # print(len(all_link))
    # print(len(all_job))
    n = 0
    for job in all_job:
        job_soup = BeautifulSoup(str(job), 'html.parser')
        job_link = job_soup.find("a", href=True)['href']
        while True:
            if job_link in all_link:
                d = all_link.index(job_link)
                # print(d)
                all_link.pop(d)
            else:
                break
        interesting_urll = base_url + job_link
        il = interesting_url(url=interesting_urll)
        il.save()
        print("Saved(interesting url) :> ", interesting_urll)
        n = n + 1
        if n == 10:
            break

    for el in all_link:
        try:
            if el[0] == '/':
                el = base_url + el
            il = non_interesting_url(url=el)
            il.save()
            print("Saved(Non interesting url) :> ", el)
        except:
            pass


def cat_to_model():
    base = os.getcwd()
    filename = os.path.join(base, 'data.xlsx')
    data = pd.read_excel(filename)
    # dh = data.head()
    interest_list = pd.DataFrame(data, columns=['Interested_Group'])
    for row in interest_list.values:
        # print(row[0])
        category = Categories(name=row[0])
        category.save()
        print("Saved(Category) :>", row[0])


def set_category(text):
    all_category = Categories.objects.all()
    for cat in all_category:
        nam = str(cat.name).lower()
        for c in nam.split():
            if c in text.lower().split():
                return nam

    return "No available category detected"


def get_details():
    int_li = interesting_url.objects.all()
    
    for url in int_li:
        try:
            m_datas = scrape(str(url.url))
            for m_data in m_datas:
                try:
                    m_data['title']
                    f_m_data = m_data
                    break
                except:
                    pass

            title = f_m_data['title']
            desc = f_m_data['description']
            dateposted = f_m_data['datePosted']
            valid = f_m_data['validThrough']
            organizatiion = f_m_data['hiringOrganization']
            try:
                place = f_m_data['jobLocation']
            except:
                place = "Not available"
            try:
                salary = f_m_data['baseSalary']
                while True:
                    if type(salary) == type({'s': "d"}):
                        salary = salary['value']
                    else:
                        break
            except:
                salary = "Data not available"

            category = set_category(str(title))

            Job = JobDB(url=url.url, title=title, description=desc,
                        salary=salary, datePosted=dateposted, validThrough=valid, hiringOrganization = organizatiion, place = place, category = category)
            Job.save()
            print("Saved(Job Details) :>", title)
        except:
            print("bad")
            pass

def manual_start():
    print("Deleting Previeus datas(if any)")
    dlt()
    print("Extracting Categories from Excel file")
    cat_to_model()
    print("Extracting Job urls from Internshala")
    internshala()
    print("Extracting Job urls from iimjobs")
    iimjobs()
    print("Extracting Job urls from Talentrack")
    talentrack()
    print("Saving Job details")
    get_details()
    print("end")


def start(request):
    print("Deleting Previeus datas(if any)")
    dlt()
    print("Extracting Categories from Excel file")
    cat_to_model()
    print("Extracting Job urls from Internshala")
    internshala()
    print("Extracting Job urls from iimjobs")
    iimjobs()
    print("Extracting Job urls from Talentrack")
    talentrack()
    print("Saving Job details")
    get_details()
    print("end")
    return HttpResponse("Scraping Completed")
