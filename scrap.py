from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from bs4 import BeautifulSoup
import requests, re
import time


# f = open('sheet.json') qqqq
# sheetID = "1wjcpzZgmnhwu-ziqynxQL2jfDiP0b6OfHiIMPBPCec8"
sheets = {
    "Cardiology":"1xZzsNnk4uUCp3CGbunBiW-0PgDW5ni44b3n-H9iGdNc",
    "Orthopaedics":"1NcDVsk1iNvhK9N_mFvILTCGs7JQHQYFS8C0qlK4wZOw",
    "Obstetrics_Gynecology":"1GUEp4C42FUpqe-dJvQztSJtakh15whye5bqghz8-6wA",
    "Oncology":"1NGSafCbjENx9DIArC3FU8cY7tXKQ1ww87l8AcfAuKLk",
    "Urology":"1zUwpSSqXftX9sv_kuT9wgtRpLU5UDqBDRf83VNacrr4",
    "Dental":"1jfbxrmlFBf6TzXq49ABn9upbahNhvxXtCQq8sezVrD4",
    "Pediatrics":"1xqP0gNXufLseMBJFNkNZ96rgJn7yt6c523eCjiKLWek",
    "Pulmonology":"1RnTJYA2t3uIpCgnjvC3UTJwxMnpNtpWGblyDGygcbdA",
    "Rheumatology":"1I0P2_GKwSJVzYLB-3c0hHIupDgwlqiC_n4rLGhPEZts",
    "Bone Marrow Transplant":"1JaJvmlgQoNKEUcPJgg6Q9VDXe-G9S1B2D7sUtY685dE",
    "Internal Medicine":"1jx6xw3AHnWjlkfp7ub3g_MpnwJ4IvKTwiGc98KgS92E",
    "Plastic Surgery":"16QjT6phrbKmEAUZPKO3PKnNG__qV4YFhh3SFvsZKM70",
    "Nephrology":"1er-mFr_JX110xJCit2NKrfJ9AbYdZkFDdFhMUffMC-Y",
    "Dermatology":"15FoSkUw3k_b6b19OpvSAv2BJB0nmGDHMsZ25nOXpTvU",
    "ENT":"1nkwTZ7OsnPPv85Q_kW-QtizZbr1mYXAXd8hNwSm9knM",
    "Opthalmology":"1SqF0mveVT3Ud-36UMGGzAgRQ1PRW6D4fGTwxq1jDQ9Q",
    "General Surgery":"1IGEExxL9fTShFCbbtjdVbL7Zt9ismAv57963xcwhaMk",
    "Bariatric":"1LGhym-VadgXGbB6sWEh-cuRDoOn7jWjNQlhxG1E6L-Q",
    "Diabetes":"1d-9K5lmooVuGLvD4QSouoafWf0OEv24KaXEgY6BcmM4",
    "Radiology":"1-qOaBbBtHIXayr_QAQWwSZB1xvSBi-YQXnzgA-yKfM0",
    "Psychiatry":"171yKR3s9TZgpuRi1rHjyCCtj9G2mnsemQF3F1aGqYG4",
    "Gastroenterology":"1YNgDT1eZWiNDs_hm80G5SPeiFwUyKXAEYaZK18gurak",
    "Neurology":"1jrvS-2tGsq3vxrqrTDW7rPpg6AA8YbfsBsV8bHLyZdc",
    "Bariatric":"1LGhym-VadgXGbB6sWEh-cuRDoOn7jWjNQlhxG1E6L-Q"
}


# print(sheetID['Hyderabad'])
# quit()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


data = {}
def getValues(sheet,sheetrange):
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = sheet
    SAMPLE_RANGE_NAME = sheetrange
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in range(1,len(values)):
            data[str(row)] = {
            "keyword": values[row][0]+" location",
            "google_soup": "",
            "searchvol_avg": int(values[row][1]),
            }
    return(data)





def google_keywords(keyword):
    final_string = {"ads_google": "", "google": ""}
    query = "https://www.google.com/search?q=" + str(keyword)
    # query = "https://www.google.com/search?q=" + str(keyword) + "&gl=in&hl=te"
    print(query)
    response = requests.get(query)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    # quit()
    mydivs = soup.findAll("div", {"class": "BNeawe vvjwJb AP7Wnd"})
    for i in range(0, len(mydivs)):
        search = (mydivs[i].find_parent("div")).find_parent("div")
        final_string["google"] += str(search).strip() + ","
    final_string["google"] = final_string["google"][0 : len(final_string["google"]) - 1]
    final_string["google"] = re.sub("'", "", str(final_string["google"]))
    # replacing double quotes with // need to change at the time of searching
    final_string["google"] = re.sub('"', "//", str(final_string["google"]))
    # print(final_string)
    # quit()
    return final_string


# print(getValues(sheetID,spec))


def start(loc,spec):
    sheetID = sheets[spec.split('-')[0]]
    getValues(sheetID,spec)
    print(data)
    for d in data.keys():
        key = re.sub("location", loc, data[d]["keyword"])
        final_string1  = google_keywords(key)
        time.sleep(15)
        data[d]["google_soup"] = final_string1["google"]
    content1 = ""
    content2 = ""
    content3 = ""
    content4 = ""
    content1 = re.sub("'", '"', str(data))
    content2 = re.sub("//", "'", str(content1))
    content3 = re.sub(r"\\xa0...", "", str(content2))
    content4 = re.sub(r"\\xa0", "", str(content3))
    print(content4)
    with open(loc+'_'+spec+'.json', "w", encoding="utf-8") as f:
        content = f.write(str(content4))
    f.close()

# spec = "Urology"
loc = "Dwarka"
# loc = "Malleshwaram"
# loc = "Old Airport Road"
# loc = "Jayanagar"
# loc = "Whitefield"
spec = "Pediatrics"+"-"+loc

start(loc,spec)     