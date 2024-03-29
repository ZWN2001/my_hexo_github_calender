# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler
import json


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def getdata(name):
    try:
        gitpage = requests.get("https://github.com/" + name)
        data = gitpage.text
        datadatereg = re.compile(r'data-date="(.*?)" data-level')
        datacountreg = re.compile(r'(\d+|No) contribution')
        datadate = datadatereg.findall(data)
        datacount = datacountreg.findall(data)
        datacount = list(map(int, [0 if i == "No" else i for i in datacount]))

        # 将datadate和datacount按照字典序排序
        sorted_data = sorted(zip(datadate, datacount))
        datadate, datacount = zip(*sorted_data)

        contributions = sum(datacount)
        datalist = []
        for index, item in enumerate(datadate):
            itemlist = {"date": item, "count": datacount[index]}
            datalist.append(itemlist)
        datalistsplit = list_split(datalist, 7)
        returndata = {
            "total": contributions,
            "contributions": datalistsplit
        }
        return returndata
    except Exception as e:
        # 返回报错
        return e




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = "ZWN2001"
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return

# getdata("ZWN2001")