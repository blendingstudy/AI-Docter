import os
from django.shortcuts import render
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate

load_dotenv()
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

def chat_llm(request):
    llm = ChatOpenAI(openai_api_key=OPEN_API_KEY)
    context = {}

    message = request.POST.get('message')  # 사용자가 제공한 메시지 가져오기
    context['user_message'] = message  # 사용자가 제공한 메시지를 context에 추가

    # Call LangChain to process the message
    if message:  # 사용자가 메시지를 제공한 경우에만 처리
        prompt = ChatPromptTemplate.from_messages(
            [
                AIMessagePromptTemplate.from_template("""
                    Please answer in Korean
                    You are an AI doctor counseling patients
                """),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )
        
        response = LLMChain(
            llm=llm, 
            prompt=prompt,
            verbose=True)
        
        context['llm_message'] = response.run(input=message)  # 언어 처리 모델로 메시지 처리 후 결과를 context에 추가

    return render(request, 'chat.html', context)

