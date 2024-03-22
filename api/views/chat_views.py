import os
from django.http import JsonResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory

load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')

#대화내용 저장 메모리
memorys: dict = {}
    
#LLM채팅 요청 API
def chat_llm(request):
    id = request.session.get('id', None)
    llm = ChatOpenAI(openai_api_key=OPEN_API_KEY)
    context = {}

    message = request.GET.get('message')  # 사용자가 제공한 메시지 가져오기
    context['user_message'] = message  # 사용자가 제공한 메시지를 context에 추가
    
    if not id in memorys:
        memorys[id] = ConversationBufferMemory(memory_key="chat_history")

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
            memory=memorys[id]
        )
        
        context['llm_message'] = response.predict(input=message)  # 언어 처리 모델로 메시지 처리 후 결과를 context에 추가

    return JsonResponse(context)

