import requests
import urllib.request, json
from datetime import date 

import pdfkit 

url = "https://radiant-oasis-51608.herokuapp.com/gmb/"
doc = "Dr. Samanjoy Mukherjee"
loc = "Dwarka"
spec = "Cardiology"


def getJSON(doc, loc):
    payload = "doc=" + doc.replace(" ", "%20") + "&loc=" + loc
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "cache-control": "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)[doc]


def getSoup(spec, loc):
    with urllib.request.urlopen(
        "https://docrank.ai/assets/json/GMB/" + spec + "/" + loc + "/" + spec + ".json"
    ) as url:
        data = json.loads(url.read().decode())

        return data


# print(getSoup(spec,doc, loc))


res_json = {}

def formJSON(doc):
    res_json[doc] = {
        "procedure": [],
        "category": [],
        "type": [],
        "gskeyword": [],
        "searchvol_avg": [],
        "gsindex": [],
        "gshits": 0,
        "gsfound": 0,
        "notfound": [],
        "nfound": 0,
    }
    return res_json

# print(res_json)
def scrap(spec,loc):
    for key, value in getSoup(spec, loc).items():
        gstemp = value["google_soup"].split("BNeawe vvjwJb AP7Wnd")
        for i in range(0, len(gstemp)):
            if gstemp[i].lower().find(doc.lower()) != -1 and res_json[doc]["gsfound"] == 0:
                res_json[doc]["gshits"] += 1
                res_json[doc]["gskeyword"].append(
                    value["keyword"].replace("location", loc) + "~" + str(value["searchvol_avg"])
                )
                res_json[doc]["gsindex"].append(i)
                res_json[doc]["gsfound"] = 1
                res_json[doc]["nfound"] = 1
                break
            res_json[doc]["gsfound"] = 0
        if res_json[doc]["gsfound"] == 0:
            res_json[doc]["notfound"].append(
                value["keyword"].replace("location", loc) + "~" + str(value["searchvol_avg"])
            )
            res_json[doc]["nfound"] = 1
    return res_json[doc]

res = {}
formJSON(doc)
res[doc]={}
res[doc]["gmb"]=getJSON(doc,loc)
res[doc]["scrap_res"] = scrap(spec,loc)
print(res)
options = {
    'page-size': 'A4',
    'quiet': '',
    'no-outline': None
    
}


# pdfkit.from_file('E:\work\GMB\HTMLIZATION.html', 'out.pdf',options=options) 
with open('E:\work\GMB\HTMLIZATION.html') as f:
    d = f.read()
    f.close()
    data = d.replace("__BNAME__",res[doc]['gmb']['bname'])
    data = data.replace("__DATE__",str(date.today()))
    data = data.replace("__LOC__",loc)
    data = data.replace("__DOC__",doc)
    # print(data)
    # quit()
    data = data.replace("__RATING__",res[doc]['gmb']['Rating'])
    data = data.replace("__REVIEWS__",res[doc]['gmb']['Reviews'])
    data = data.replace("__BCAT__",res[doc]['gmb']['category'])
    data = data.replace("__ADD__",res[doc]['gmb']['address'])
    data = data.replace("__AUTH__",res[doc]['gmb']['authority'])
    data = data.replace("__PHN__",'')
    data = data.replace("__OPNHRS__",res[doc]['gmb']['openhours'])
    t = ''
    for i in range(0,len(res[doc]['scrap_res']['gskeyword'])):
        print(res[doc]["scrap_res"]["gskeyword"][i].split("~")[0])
        t = t+'<tr><td  style="font-family: arial; font-size: 14px; line-height: 18px; color: #000000; border-top: 2px solid #dbdbdb; padding: 5px;padding-left:30px ">'+res[doc]["scrap_res"]["gskeyword"][i].split("~")[0]+' </td><td  style="font-family: arial; font-size: 14px; line-height: 18px; color: #000000; border-top: 2px solid #dbdbdb; padding: 5px;">'+res[doc]["scrap_res"]["gskeyword"][i].split("~")[1]+' </td><td  style="font-family: arial; font-size: 14px; line-height: 18px; color: #000000; border-top: 2px solid #dbdbdb; padding: 5px;">'+str(res[doc]['scrap_res']['gsindex'][i])+'</td></tr>'
    data = data.replace("__FOUND__",t)
    nt = ''
    rc = ''

    for i in range(0,len(res[doc]['scrap_res']['notfound'])):
        nt = nt+'<tr><td   style="font-family: arial; font-size: 14px; line-height: 18px; color: #000000; border-top: 2px solid #dbdbdb; padding: 5px; padding-left:30px">'+res[doc]["scrap_res"]["notfound"][i].split("~")[0]+' </td><td   style="font-family: arial; font-size: 14px; line-height: 18px; color: #000000; border-top: 2px solid #dbdbdb; padding: 5px;">'+res[doc]["scrap_res"]["notfound"][i].split("~")[1]+' </td>        <td  style="font-family: arial; font-size: 14px; line-height: 18px; color: #000000; border-top: 2px solid #dbdbdb; padding: 5px;">-</td></tr>'
        if(i<=3):
            rc = rc+ '<tr><td align="left" valign="top" style="font-family: arial; font-size: 18px; line-height: 22px; color: #333234; padding-top: 5px;"><b>&bull;' +res[doc]["scrap_res"]["notfound"][i].split("~")[0]+' </b></td></tr>'
    data = data.replace("__NOT__",nt)
    data = data.replace("__REC__",rc)


    # print((data))
    pdfkit.from_string(str(data), doc+'.pdf',options=options)
# pdfkit.from_url('http://google.com', 'out.pdf')