import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
import db

db = db.get_db()


# 갱신일자 : 1일 1번
# 첫 갱신 후 수정 하지 않도록 설정
def include_centers():
    db.centers.delete_many({})

    page = 1
    perPage = 1000
    encoding_key = "sopjfpWYV6pdBmu8EUQVJWkAokTomNvzK4zMcYGUjvudoSgiOvB16V86LXzfjna9Yg9xYmFtN6qyQf2N7pWEJw%3D%3D"
    result = list()

    url = 'https://api.odcloud.kr/api/15077586/v1/centers'
    queryParams = '?' + \
                  f'page={page}' + \
                  f'&perPage={perPage}' + \
                  f'&serviceKey={encoding_key}'
    query_url = url + queryParams

    """
    "address": "광주광역시 동구 필문대로 365",
    "centerName": "코로나19 호남권역 예방접종센터",
    "centerType": "중앙/권역",
    "createdAt": "2021-03-03 07:00:52",
    "facilityName": "조선대학교병원 의성관 5층",
    "id": 3,
    "lat": "35.139465",
    "lng": "126.925563",
    "org": "조선대병원",
    "phoneNumber": "062-220-3739",
    "sido": "광주광역시",
    "sigungu": "동구",
    "updatedAt": "2021-06-02 07:32:04",
    "zipCode": "61452"
    
    
    """

    r = requests.get(query_url)
    rjson = r.json()

    for json_data in rjson["data"]:
        id = json_data['id']  # 예방 접종 센터 고유 식별자
        centerName = json_data["centerName"]  # 예방 접종 센터 명
        sido = json_data['sido']  # 시도
        sigungu = json_data['sigungu']  # 시군구
        facilityName = json_data['facilityName']  # 시설명
        zipCode = json_data['zipCode']  # 우편번호
        address = json_data["address"]  # 주소
        lat = json_data['lat']  # 좌표(위도)
        lng = json_data['lng']  # 좌표(경도)
        centerType = json_data["centerType"]  # 예방 접종 센터 유형
        org = json_data['org']  # 운영기관
        phoneNumber = json_data['phoneNumber']  # 사무실 전화번호
        createdAt = json_data['createdAt']  # 센터 등록 날짜
        updatedAt = json_data['updatedAt']  # 센터 수정 날짜

        db.centers.insert_one(json_data)


""" 
  논리 구현
 # 이루어 져야할 것 : 서버의 시간 동기화 가 현실의 시간과 동일한가?
  - 해결 방안 utck로 서버의 시간을 동기화 시킨 후 운영을 시작하도록 사전 설정을 해야한다.
 1. baseDate와 datetime.now()를 비교하여 datetime.now()가 baseDate보다 더 크다면 
 2. 오늘 날짜로 api를호출한다.
 3. 호출한 api의 데이터가 존재하지 않다면 == (아직까지 api 갱신이 이루어 지지 않았다면) 
 4 - 1 . return으로 api 갱신을 멈춘다.
 4 - 2. 만약 호출한 api의 데이터가 존재한다면
 5. 현재 DB의 데이터를 Delete하고, 호출한 api데이터를 insert 한다
"""


# 갱신 일자 : 9시45 ~ 10시
# 12시 기점으로 갱신할 것
def include_statistics():
    db.statistics.delete_many({})
    page = 1
    perPage = 1000
    now = datetime.now()
    encoding_key = "sopjfpWYV6pdBmu8EUQVJWkAokTomNvzK4zMcYGUjvudoSgiOvB16V86LXzfjna9Yg9xYmFtN6qyQf2N7pWEJw%3D%3D"
    result = list()

    url = "https://api.odcloud.kr/api/15077756/v1/vaccine-stat"
    queryParams = '?' + \
                  f'page={page}' + \
                  f'&perPage={perPage}' + \
                  f"&cond%5BbaseDate%3A%3AEQ%5D={now.strftime('%Y-%m-%d')} 00:00:00" + \
                  f'&serviceKey={encoding_key}'
    query_url = url + queryParams
    r = requests.get(query_url)
    rjson = r.json()

    # 당일날의 데이터가 갱신되지 않았을 경우 이전날의 데이터를 가지고 온다.
    if rjson['currentCount'] <= 0:
        now = now - timedelta(days=1)
        queryParams = '?' + \
                      f'page={page}' + \
                      f'&perPage={perPage}' + \
                      f"&cond%5BbaseDate%3A%3AEQ%5D={now.strftime('%Y-%m-%d')} 00:00:00" + \
                      f'&serviceKey={encoding_key}'
        query_url = url + queryParams
        r = requests.get(query_url)
        rjson = r.json()

    """
    accumulatedFirstCnt : 7600157
    accumulatedSecondCnt : 2279997
    baseDate : 2021-06-08 00:00:00
    firstCnt : 855642
    secondCnt : 19856
    sido : 전국
    totalFirstCnt : 8455799
    totalSecondCnt : 2299853
    """

    for json_data in rjson['data']:
        baseDate = json_data['baseDate']  # 통계 기준일자
        sido = json_data['sido']  # 지역명칭
        firstCnt = json_data['firstCnt']  # 당일 통계(1차 접종)
        secondCnt = json_data['secondCnt']  # 당일 통계(2차 접종)
        totalFirstCnt = json_data['totalFirstCnt']  # 전체 누적 통계(1차 접종)
        totalSecondCnt = json_data['totalSecondCnt']  # 전체 누적 통계(2차 접종)
        accumulatedFirstCnt = json_data['accumulatedFirstCnt']  # 전일까지의 누적 통계 (1차 접종)
        accumulatedSecondCnt = json_data['accumulatedSecondCnt']  # 전일까지의 누적 통계 (2차 접종)

        db.statistics.insert_one(json_data)
