from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

#정적페이지 크롤링에 사용되는 라이브러리인 BeautifulSoup를 임포트
#url정보를 요청하는 urllib.request를 임포트
#데이터시각화를 위한 pandas 임포트

# [CODE 1]
def hollys_store(result):
    for page in range(1, 59): #실제 할리스홈페이지에 매장 정보가 58페이지까지 있으므로
        #1~58페이지까지 반복해서 url 설정

        Hollys_url = 'https://www.hollys.co.kr/store/korea/korStore.do?pageNo=%d&sido=&gugun=&store=' % page
        #크롤링하기 위한 url 설정
				#위에서 언급한대로 url의 페이지 부분만 바꿔가며 사용

        print(Hollys_url)

        html = urllib.request.urlopen(Hollys_url)
        #urllib.request의 urlopen메소드를 사용해서 해당 페이지서버에 요청을 보내어 받은 응답을 객체로 반환


        soupHollys = BeautifulSoup(html, 'html.parser')
        #해당 객체를 BeautifulSoup를 통해 html태그를 인식한 soup객체로 반환


        tag_tbody = soupHollys.find('tbody')
        #tbody태그를 찾음


        for store in tag_tbody.find_all('tr'):
            #tr태그들에 각 매장들의 정보가 담겨있으므로
            #tbody태그 안에 있는 모든 tr태그들을 찾은 다음
            #store변수로 순회


            #tr태그 안에 있는 내용의 갯수가 3개 이하라면 for문을 중지합니다
            if len(store) <= 3:
                break

            #tr태그 안에 td태그들에 매장이름,시 도 ,주소 , 전화번호 등의 정보가 담겨 있으므로
            #store_td에서 td태그들을 각각 찾은 다음
            #그 내용들을 .string으로 추출합니다

            store_td = store.find_all('td')
            store_name = store_td[1].string
            store_sido = store_td[0].string
            store_address = store_td[3].string
            store_phone = store_td[5].string
            result.append([store_name] + [store_sido] + [store_address]
                          + [store_phone])
            #최종 결과값들을 담고 있는 result배열에 append 해줍니다
    return


# [CODE 0]
def main():
    result = []
    print('Hollys store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    hollys_store(result)

    hollys_tbl = pd.DataFrame(result, columns=('store', 'sido-gu', 'address', 'phone'))
    #결과값(result)을 바탕으로 pandas를 사용합니다
    #각 속성값을 'store', 'sido-gu', 'address', 'phone' 로 지정해 줍니다
		#result배열의 값은 각각 순서대로 매장이름,시도,주소,전화번호 이렇게 들어가 있으므로
		#판다스의 속성값 또한 순서대로 맞게 작성한 것입니다

    hollys_tbl.to_csv('./6장_data/hollys.csv', encoding='cp949', mode='w', index=True)
    #테이블을 CSV 파일로 저장합니다
    #현재 이 파이썬 파일이 있는 디릭토를 기준으로 '/6장_data/hollys.csv' 형태로 저장을 해 줍니다 (파일명 hollys.csv)


    del result[:]
    #이건 뭐지?


if __name__ == '__main__':
    main()