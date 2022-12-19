import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey = "Unrj3C%2B1Q7LoxSlJVzf81Xe9bVu4Ll3H91Fgx11%2BYTGi3NP2KrqOJLfEAN025uQiKMW1reyLfOeKKeJDOg68PA%3D%3D"


def getHomePriceFirst():
    url = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=OGVkZTYwNzk0YWI4ZGFkZDdlY2YwNjMyOTY1NjcxNzk=&itmId=H001+&objL1=A002+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&newEstPrdCnt=10&orgId=110&tblId=DT_11001N_2013_A010'

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            # print("[%s] Url Request Success" % datetime.datetime.now())
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(e)
        # print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None



def getHomePriceSecond():
    url = 'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=OGVkZTYwNzk0YWI4ZGFkZDdlY2YwNjMyOTY1NjcxNzk=&itmId=H001+&objL1=A002+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&newEstPrdCnt=10&orgId=110&tblId=DT_11001N_2013_A010A'

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            # print("[%s] Url Request Success" % datetime.datetime.now())
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(e)
        # print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def convertToCsv():
    homePrices=[]
    result = []
    jsonData = getHomePriceFirst()
    for i in range(len(jsonData)):
        number=float(jsonData[i]['DT'])
        homePrices.append(round(number))
    jsonData = getHomePriceSecond()
    for i in range(len(jsonData)):
        number =float(jsonData[i]['DT'])
        homePrices.append(round(number))

    # 파일저장 2 : csv 파일
    columns = ["HomePrice"]
    result_df = pd.DataFrame(homePrices, columns=columns)
    result_df.to_csv('homePrice.csv',
                     index=False, encoding='cp949')

def main():
    getHomePriceFirst()
    getHomePriceSecond()
    convertToCsv()


if __name__ == '__main__':
    main()