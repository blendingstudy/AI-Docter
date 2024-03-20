import os
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from django.shortcuts import render
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory

load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

#대화내용 저장 메모리
memory = ConversationBufferMemory(memory_key="chat_history")
    
#LLM채팅 요청 API
def chat_llm(request):
    llm = ChatOpenAI(openai_api_key=OPEN_API_KEY)
    context = {}

    message = request.GET.get('message')  # 사용자가 제공한 메시지 가져오기
    context['user_message'] = message  # 사용자가 제공한 메시지를 context에 추가

    if message:  # 사용자가 메시지를 제공한 경우에만 처리
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template("""
                    Please answer in Korean
                    You are an AI doctor counseling patients
                    {chat_history}
                """),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )
        
        response = LLMChain(
            llm=llm, 
            prompt=prompt,
            verbose=True,
            memory=memory
        )
        
        context['llm_message'] = response.predict(input=message)  # 언어 처리 모델로 메시지 처리 후 결과를 context에 추가

    return JsonResponse(context)

