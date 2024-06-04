import os
import json
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from rest_framework.decorators import api_view
from openai import OpenAI
from openai import OpenAIError, APIConnectionError, RateLimitError, APIStatusError

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_completion(prompt):
    print(prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        completion = response.choices[0].message.content
        print(completion)
        return completion
    except (APIConnectionError, RateLimitError, APIStatusError) as e:
        print(f"API Error: {e}")
        raise
    except OpenAIError as e:
        print(f"OpenAI Error: {e}")
        raise

@api_view(['POST'])
def query_view(request):
    try:
        data = request.data
        prompt = data.get('prompt', '')
        if not prompt:
            return JsonResponse({'error': 'No prompt provided'}, status=400)
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    except OpenAIError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#-----------------------------------------------------------------------#
def send_kakao_message(text):
    with open("kakao_token.json", "r") as json_file:
        tokens = json.load(json_file)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }
    py_data = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://n.news.naver.com/mnews/article/030/0003211565",
            "mobile_web_url": "https://n.news.naver.com/mnews/article/030/0003211565"
        }
    }
    data = {
        "template_object": json.dumps(py_data)
    }
    response = requests.post(url, headers=headers, data=data)
    
    print(response.status_code)  # Print response status code

    if response.json().get('result_code') == 0:
        print("메시지를 성공적으로 보냈습니다! :)")
    else:
        print("메시지를 성공적으로 보내지 못했습니다. 오류메시지 : " + str(response.json()))
    
    return response.json()

@api_view(['GET'])
def send_message_view(request):
    try:
        response = send_kakao_message("우린 멋사 12기야~")
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#-----------------------------------------------------------------------#
@api_view(['POST'])
def summarize_and_send_news(request):
    try:
        data = request.data
        news_content = data.get('news', '')
        
        if not news_content:
            return JsonResponse({'error': 'No news content provided'}, status=400)
        
        # 뉴스 요약
        prompt = f"Summarize the following news in Korean: {news_content}"
        summary = get_completion(prompt)
        
        # 요약된 뉴스를 카카오톡으로 전송
        response = send_kakao_message(summary)
        return JsonResponse({'summary': summary, 'kakao_response': response})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)