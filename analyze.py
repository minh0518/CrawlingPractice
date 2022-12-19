from scipy import stats
from statsmodels.formula.api import ols, glm
import urllib.request
import json
import pandas as pd
from bs4 import BeautifulSoup
#시각화
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import urllib.request
import datetime


import ssl


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


def getHomePrice():
    getHomePriceFirst()
    getHomePriceSecond()
    convertToCsv()
    return pd.read_csv('homePrice.csv', encoding='cp949')


def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)

    try:
        ssl.create_default_https_context = ssl._create_unverified_context  # 접속보안 허용

        response = urllib.request.urlopen(req)
        if response.getcode() == 200:  # 성공시
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')

            return ret

    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def interest_address():
    firstResult = []
    secondResult = []
    base_rate_url = 'https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643'

    rcv_data = get_request_url(base_rate_url)
    soupData = BeautifulSoup(rcv_data, 'html.parser')
    tag_tbody = soupData.find('tbody')

    tmp=[]
    for case in reversed(tag_tbody.find_all('tr')):
        case_td = case.find_all('td')
        case_year = int(case_td[0].string)
        case_rate = float(case_td[2].string)
        if (case_year in tmp) :
            continue
        tmp.append(case_year)

        if(case_year >= 2009 and case_year <= 2013):
            firstResult.append(['09~13', case_year, case_rate])



        elif(case_year > 2013 and case_year <= 2019):
            secondResult.append(['14~19', case_year, case_rate])


    return [firstResult, secondResult]

def getYearRate():
    [firstResult, secondResult] = interest_address()
    firstInterest = pd.DataFrame(firstResult, columns=('classify', 'year', 'rate'))
    firstInterest.to_csv('firstInterest.csv', encoding='cp949', mode='w', index=False)
    secondResult = pd.DataFrame(secondResult, columns=('classify', 'year', 'rate'))
    secondResult.to_csv('secondInterest.csv', encoding='cp949', mode='w', index=False)

    rate = pd.concat([firstInterest, secondResult])
    rate.to_csv('rate.csv', encoding='cp949', mode='w', index=False)

    return pd.read_csv('rate.csv', encoding='cp949')

def getYearGDP():
    return pd.read_csv('yearGDP.csv', encoding='cp949')


def getYearHousingSupply():
    return pd.read_csv('yearHousingSupply.csv')


#분석
def calc(yearRate, yearGDP, yearHousingSupply, homePrice):
    info = pd.concat([yearRate, yearGDP, yearHousingSupply, homePrice], axis=1)

    # 숫자 변환
    householdsData = info['households']
    for i in householdsData.index:
        str = info['households'][i]
        traget = str.replace(',', '')
        info.at[i, 'households'] = int(traget)

    houseData = info['house']
    for i in houseData.index:
        str = info['house'][i]
        traget = str.replace(',', '')
        info.at[i, 'house'] = int(traget)

    info.to_csv('info.csv', index=False, encoding='cp949')

    info = pd.read_csv('info.csv', encoding='cp949')

    print(info.describe())

    firstClassify = info.loc[info['classify'] == '09~13', 'HomePrice']
    secondClassify = info.loc[info['classify'] == '14~19', 'HomePrice']

    stats.ttest_ind(firstClassify, secondClassify, equal_var=False)

    Rformula = 'HomePrice ~ rate + GDP + EconomicGrowth +households + house + HousingSupply'

    regression_result = ols(Rformula, data=info).fit()
    print(regression_result.summary())

    sample1 = info[info.columns.difference(['HomePrice','classify'])]
    sample1 = sample1[0:5][:]
    sample1_predict = regression_result.predict(sample1)
    print(sample1_predict)

    print(info[0:5]['HomePrice'])

    data = {"year": [2012, 2013], "rate": [1.77, 1.35], "GDP": [1654, 1739], "EconomicGrowth": [2.8, 2.9],"households": [3783, 3785],"house": [3634, 3643], "HousingSupply": [95, 96.1]}

    sample2 = pd.DataFrame(data, columns=sample1.columns)
    print(sample2)

    sample2_predict = regression_result.predict(sample2)
    print(sample2_predict)

def main():
    homePrice=getHomePrice()
    yearRate=getYearRate()
    yearGDP = getYearGDP()
    yearHousingSupply =getYearHousingSupply()
    calc(yearRate, yearGDP, yearHousingSupply, homePrice)


if __name__ == '__main__':
    main()