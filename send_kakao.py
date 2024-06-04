from dotenv import load_dotenv
import os
import requests
import json

with open("kakao_token.json", "r") as json_file:
    tokens = json.load(json_file)
# 토큰 response를 담은 json 파일을 tokens라는 변수로 불러와 담아줍시다.
# 카카오톡 메모 보내기 API의 엔드포인트 URL을 정의한다.
url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 요청에 포함될 헤더를 정의한다.
# 토큰 형식 인증임을 예고하는 "Bearer"와 그 상황에 해당하는 실제 액세스 토큰을 조합하여 헤더에 싣는다.
headers = {
    "Authorization": "Bearer " + tokens["access_token"]
}

# "template_object" 필드에 JSON 형태의 템플릿 객체를 문자열로 인코딩하여 전송한다.
py_data = {
    "object_type": "text",  # 템플릿 객체의 타입을 지정한다.
    "text": "우린 멋진 친구야.",  # 템플릿 객체의 텍스트 내용을 지정한다.
    "link": {  # 템플릿 객체의 링크 정보를 지정한다.
        "web_url": "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=친구",
        "mobile_web_url": "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=친구"
    }
}

data = {
    "template_object": json.dumps(py_data)
}

response = requests.post(url, headers=headers, data=data) # POST 요청을 보내고 응답을 받아온다.

print(response.status_code) # 응답의 상태코드를 출력한다.

if response.json().get('result_code') == 0: # 응답받은 JSON 객체에서 'result_code' 값이 0인 경우
    print("메시지를 성공적으로 보냈습니다! :)")
else: # 오류메시지와 함께 응답받은 JSON 객체를 문자열로 변환하여 출력한다.
    print("메시지를 성공적으로 보내지 못했습니다. 오류메시지 : " + str(response.json()))

# 대리경유 사용자 정보 조회(기본 정보 및 각종 항목 등의 여부 출력)
info_url = "https://kapi.kakao.com/v2/user/scopes" # Kakao API를 이용하여 사용자 정보 조회를 위한 URL
params = {"secure_resource": True} # API 요청 시 필요한 파라미터
info_res = requests.get(info_url, headers=headers, params=params) # 사용자 정보 조회(GET) 요청을 보내고 응답을 받아온다.

print(info_res.json()) # 사용자 정보 조회 결과를 JSON 형태로 출력
