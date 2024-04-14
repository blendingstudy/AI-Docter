import json
import xml.etree.ElementTree as ET

import requests
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores.chroma import Chroma
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.aidocter.models.chat_history import ChatHistory
from app.aidocter.models.chat_list import ChatList
from common.utils import Utils
from common.searchApi import SearchApi

llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
api = SearchApi()
memorys: dict = {}  #대화내용 저장 메모리


#LLM채팅 요청 API
@require_POST
def chat_llm(request):
    user = request.user
    data = json.loads(request.body)
    chat_list_id = data.get('chatId')
    message = data.get('message')  # 사용자가 제공한 메시지 가져오기
    result = {}


    print(message)
    print(chat_list_id)

    search_result = api.google_api(message)

    result['user_message'] = message  # 사용자가 제공한 메시지를 context에 추가

    if message:  # 사용자가 메시지를 제공한 경우에만 처리
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("""
                Please answer in Korean
                You are an AI doctor counseling patients

                
                
                {history}
            """),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])

        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memorys[user][chat_list_id]
        )

        # 언어 처리 모델로 메시지 처리 후 결과를 context에 추가
        result['llm_message'] = chain.run(input=message)

        # ChatHistory 모델을 사용하여 대화 내용 저장
        ChatHistory.objects.create(
            chat_list_id=chat_list_id,
            username=str(user),
            message=message,
            div='user'
        )
        ChatHistory.objects.create(
            chat_list_id=chat_list_id,
            username='llm',
            message=result['llm_message'],
            div='llm'
        )

        chat_hist = ChatHistory.objects.filter(chat_list_id=chat_list_id).order_by('-id').first()

        ChatList.objects.filter(id=chat_list_id).update(last_message=chat_hist.message)

    return JsonResponse(result)


@require_POST
def set_chat_history(request):
    user = request.user
    data = json.loads(request.body)
    chat_list_id = data.get('chatId')
    result = []

    chat_history = ChatHistory.objects.filter(chat_list_id=chat_list_id).order_by('id')

    if user not in memorys:
        memorys[user] = {}

    if chat_list_id not in memorys[user]:
        # ChatHistory 모델에서 chat_list_id로 조회
        memory = ConversationBufferWindowMemory()

        if chat_history.exists():
            # 조회 결과가 있는 경우에만 ConversationBufferMemory에 값 할당
            for chat in chat_history:
                if chat.div == 'user':
                    memory.chat_memory.add_user_message(chat.message)
                elif chat.div == 'llm':
                    memory.chat_memory.add_ai_message(chat.message)

        memorys[user][chat_list_id] = memory

    chat_history_data = serializers.serialize('json', chat_history)

    json_data = json.loads(chat_history_data)

    result = []

    # 데이터 파싱
    for item in json_data:
        pk = item['pk']
        fields = item['fields']
        parsed_data = {
            'pk': pk,
            'username': fields['username'],
            'message': fields['message']
        }
        result.append(parsed_data)

    # 결과를 JSON 형태로 변환
    json_result = json.dumps(result, ensure_ascii=False)

    print(json_result)

    return HttpResponse(json_result)


@require_GET
def get_hospital(request):
    url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'
    params = {
        'serviceKey': settings.HOSPITAL_API_KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'sidoCd': '110000',
        'sgguCd': '110019',
        'emdongNm': '신내동',
        'yadmNm': '서울의료원',
        'zipCd': '2010',
        'clCd': '11',
        'dgsbjtCd': '01',
        'xPos': '127.09854004628151',
        'yPos': '37.6132113197367',
        'radius': '3000'
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        xml_data = response.content  # XML 응답 데이터
        root = ET.fromstring(xml_data)  # XML 데이터를 파싱하여 ElementTree 객체 생성

        # 딕셔너리로 변환된 XML 데이터
        data_dict = Utils.xml_to_dict(root)
        print(data_dict)
        return HttpResponse(data_dict)
    else:
        return HttpResponse(response.status_code)


@require_GET
def get_disease(request):
    url = 'http://apis.data.go.kr/B551182/diseaseInfoService/getDissNameCodeList'
    params = {
        "serviceKey": settings.DISEASE_APY_KEY,
        "numOfRows": "10",
        "pageNo": "1",
        "sickType": "1",
        "medTp": "1",
        "diseaseType": "SICK_NM",
        "searchText": "감기"
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        xml_data = response.content  # XML 응답 데이터
        root = ET.fromstring(xml_data)  # XML 데이터를 파싱하여 ElementTree 객체 생성

        # 딕셔너리로 변환된 XML 데이터
        data_dict = Utils.xml_to_dict(root)
        print(data_dict)
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    else:
        print('Error:', response.content)
        return HttpResponse(response.status_code)


@require_GET
def set_chroma(request):
    question = request.GET.get('question')

    db = Chroma(embedding_function=embeddings, persist_directory="chroma_db")

    # df = pd.read_excel('static/file/컬럼정보_코드.xls')
    # # 열 제목 추출
    # column_names = df.columns.tolist()

    # # DataFrame의 각 행을 열 제목과 함께 텍스트로 변환
    # texts = []
    # for _, row in df.iterrows():
    #     row_dict = {col: str(val) for col, val in zip(column_names, row.astype(str))}
    #     texts.append(json.dumps(row_dict, ensure_ascii=False))

    # print(texts)
    # metadatas = [{'index': idx} for idx in df.index]
    # db.add_texts(texts, metadatas=metadatas)

    retriever = db.as_retriever()
    test = retriever.get_relevant_documents(question)
    print(test)

    return HttpResponse(test)


@require_GET
def search_google(request):
    question = request.GET.get('question')
    print("질문: " + question)
    result = api.google_api(question)
    print(result)

    return HttpResponse(result)


@require_GET
def search_naver(request):
    question = request.GET.get('question')
    print("질문: " + question)
    result = api.naver_api(question)
    print(result)

    return HttpResponse(result)
