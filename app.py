
  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import time
from threading import Thread
import threading
import pprint
from selenium.common.exceptions import NoSuchElementException
import os
import pandas
from bs4 import BeautifulSoup
import json

mydict = {}
# mydict = {"saroj": {"2019": {"12": {"Rating": "NA", "Reviews": "NA"}}}}

options = Options()
options.headless = True
x = datetime.datetime.now()
driver = webdriver.Chrome(
        options=options
    )

def getdata(driver,docname):
    mydict[docname] = {}
    try:
        if(len(driver.find_elements_by_css_selector("h1.section-hero-header-title-title.GLOBAL__gm2-headline-5"))!=0):
            bname = driver.find_element_by_css_selector("h1.section-hero-header-title-title.GLOBAL__gm2-headline-5").text
            mydict[docname]["bname"]= bname
        else:
            mydict[docname]["bname"]= "NA"
        if(len(driver.find_elements_by_css_selector("button.widget-pane-link"))!=0):
            cat = driver.find_elements_by_css_selector("button.widget-pane-link")
            for i in range(0,len(cat)):
                if(cat[i].get_attribute("jsaction") == "pane.rating.category"):
                    category = cat[i].text
                    mydict[docname]["category"]= category
        else:
            mydict[docname]["category"]= "NA"

        if(len(driver.find_elements_by_css_selector("span.section-star-display"))!=0):
            rating = driver.find_element_by_css_selector("span.section-star-display").text
            mydict[docname]["Rating"]= rating
        else:
            mydict[docname]["Rating"]= "NA"
        if(len(driver.find_elements_by_css_selector("span.section-rating-term"))!=0):
            reviews = driver.find_element_by_css_selector("span.section-rating-term").text.strip("()")
            mydict[docname]["Reviews"] = reviews
        else:
            mydict[docname]["Reviews"] = "NA"
        if(len(driver.find_elements_by_css_selector("div.section-open-hours-container"))!=0):
            openhours = driver.find_element_by_css_selector("div.section-open-hours-container").get_attribute("aria-label")
            openhours = openhours.replace("Hide open hours for the week","")
        else:
            openhours = "NA"
        mydict[docname]["openhours"]=openhours
        allattr = driver.find_elements_by_css_selector("button.ugiz4pqJLAG__button")
        # print(allattr)
        for i in range(0,len(allattr)):
            try:
                data = allattr[i].get_attribute("aria-label")
                dataid = allattr[i].get_attribute("data-item-id")
                # print(dataid+"~"+data)
                if(data !=None):
                    if(dataid == "address"):
                        data = data.replace("Address:","")
                    elif("phone" in dataid):
                        dataid = dataid.split(":")[0]
                        data = data.replace("Phone:","")
                    elif(dataid == "authority"):
                        data = data.replace("Website:","")
                    mydict[docname][dataid] = data
            except Exception as e:
                continue
        if(len(driver.find_elements_by_css_selector("div.section-local-post"))!=0):
            localpost = driver.find_element_by_css_selector("div.section-local-post")
            localpost.click()
            time.sleep(5)
            driver.execute_script("document.getElementsByClassName('scrollable-show')[0].scrollTo(0,5000)")
            time.sleep(10)
            driver.execute_script("document.getElementsByClassName('scrollable-show')[0].scrollTo(0,5000)")
            time.sleep(5)
            posts = driver.find_elements_by_css_selector("div.section-local-post-expanded")
            time.sleep(5)
            print(len(posts))
            
            mydict[docname]["posts"]=[]
            for i in range(0,len(posts)):
                print(i)
                soup = BeautifulSoup(posts[i].get_attribute('outerHTML'), "html.parser")
                print(soup.select_one("div.section-local-post-expanded").text)
                print("======================")
                datta={}
                datta["merchant"] = soup.select_one("div.section-local-post-expanded-merchant-name").text
                datta["postedon"] = soup.select_one("div.section-local-post-expanded-merchant-subtitle").text
                datta["imgurl"] = soup.select_one("div.media-container > img")['src']
                datta["summary"] = soup.select_one("div.section-local-post-expanded-summary").text
                mydict[docname]["posts"].append(datta)



            mydict[docname]["localpost"] = "Yes"
            mydict[docname]["localpost_content"] = localpost.text.strip()
        else:
            mydict[docname]["localpost"] = "No"
            mydict[docname]["localpost_content"] = "NA"
        return mydict
    except Exception as e:
        print(e)

def start(myurl, docname):
    print(myurl)
    driver.get(myurl)
    # time.sleep(3)
    # driver.find_element_by_id("searchbox-searchbutton").click()
    time.sleep(5)
    if (
        len(
            driver.find_elements_by_css_selector(
                ".section-hero-header-title-description"
            )
        )
        != 0
    ):
        getdata(driver,docname)
    else:
        mainlist = ["manipal"]
        print("in diiferent case")
        maindiv = driver.find_elements_by_css_selector("div.section-result")
        for i in range(0,len(maindiv)):
            # print(maindiv[i].text)
            if(len(maindiv[i].find_elements_by_css_selector("span.section-result-location"))!=0):
                loc = maindiv[i].find_element_by_css_selector("span.section-result-location").text
            else:
                loc = "~"
            if(len(maindiv[i].find_elements_by_css_selector("div.section-result-action-container >div > a"))!=0):
                website = maindiv[i].find_element_by_css_selector("div.section-result-action-container > div > a").get_attribute("href") if maindiv[i].find_element_by_css_selector("div.section-result-action-container > div > a").get_attribute("href")!=None else  "~"
            else:
                website = '~'
            if(len(maindiv[i].find_elements_by_css_selector("h3.section-result-title > span"))!=0):
                name = maindiv[i].find_element_by_css_selector("h3.section-result-title > span").text
            else:
                name = '~'
            boo = any(ele in website.lower() for ele in mainlist)
            loo = any(e in loc.lower() for e in mainlist)
            print(boo,loo,docname.lower() in name.lower())
            if((loo or boo)  and (docname.lower() in name.lower())):
                print('in')
                maindiv[i].click()
                break
        time.sleep(10)
        getdata(driver,docname)
        
    return mydict

location = "delhi"
doctors = [
    # "manipal hospital",
    # "Dr. Vedant Kabra- HOD Surgical Oncology",
    # "Dr Vedant Kabra Cancer Surgeon",
    # "Dr. Rajeev Verma- HOD, Joint Replacement, Orthopaedic Surgeon, Delhi",
    # "DR KUNAL DAS - BEST Gastroenterologist, Liver Specialist and Endoscopy Doctor in Delhi",
    # "Dr Lovkesh Anand, Liver Specialist in Dwarka, Gastroenterologist in Dwarka, Endoscopy",
    # "Dr Vedant Kabra Cancer Surgeon",
    # "Dr Peush Bajpai, Best Medical Oncologist Delhi, Myeloma, Prostate,Lung,Bone,Breast Cancer Specialist",
    # "Dr. Anusheel Munshi - HOD, Radiation Oncology, Delhi",
    # "Dr Sunny Garg - Medical Oncologist",
    # "Dr. Leena N Sreedhar",
    "Dr Arvind Sabharwal"
    # "Dr. Yashica Gudesar",
    # "Dr. Vikas Taneja",
    # "Dr. Saurabh Pokhariyal",
    # "Dr Puneet Khanna, Chest Specialist, Respiratory Medicine, Delhi",
    # "Dr. Vikas Gupta | Best Spine Surgeon/Neurosurgeon in Delhi, India | Brain Tumor Specialist",
    # "Dr. Khushbu Goel",
    # "Dr Vineet surana",
    # "Dr Davinder Kundra",
    # "Dr Manoj Gupta",
    # "Dr. Rajeev Verma",
    # "Dr Saurabh Verma",
    # "dr davinder kundra"
    # "Dr Gaurav Rastogi"
]
threads = []
for docname in doctors:
    myhosp = docname + " " + location
    # myurl = "https://www.google.com/maps/place/" + myhosp
    myurl = "https://www.google.com/maps/search/" + myhosp+"/@28.6283815,77.0746765,13z/data=!3m1!4b1"

    res = start(myurl,docname)
driver.close()
print(res)
pandas.read_json(json.dumps(res)).to_csv('res.csv')

