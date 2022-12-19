from scipy import stats
from statsmodels.formula.api import ols, glm
import urllib.request
import json
import pandas as pd

#시각화
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


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

def getYearRate():
    return pd.read_csv('yearRate.csv')

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


    housePrice = info['HomePrice']

    stats.ttest_ind(housePrice, housePrice, equal_var=False)

    Rformula = 'HomePrice ~ rate + GDP + EconomicGrowth +households + house + HousingSupply'

    regression_result = ols(Rformula, data=info).fit()
    print(regression_result.summary())

    sample1 = info[info.columns.difference(['HomePrice'])]
    sample1 = sample1[0:5][:]
    sample1_predict = regression_result.predict(sample1)
    # print(sample1_predict)
    #
    # print(info[0:5]['HomePrice'])

    data = {"rate": [2.4, 2.1], "GDP": [1205, 1500], "EconomicGrowth": [7.3, 7.1], "households": [3243, 3921],
            "house": [4023, 2999], "HousingSupply": [93.2, 96.3]}

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