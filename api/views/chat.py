import os
from django.http import JsonResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from aidocter.models.chat_history import ChatHistory

load_dotenv()

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
llm = ChatOpenAI(openai_api_key=OPEN_API_KEY)

#대화내용 저장 메모리
memorys: dict = {}
    
#LLM채팅 요청 API
def chat_llm(request):
    user = request.user
    chat_list_id = request.GET.get('chatId')
    message = request.GET.get('message')  # 사용자가 제공한 메시지 가져오기
    context = {}

    context['user_message'] = message  # 사용자가 제공한 메시지를 context에 추가
    
    if not user in memorys:
        memorys[user] = ConversationBufferMemory(memory_key="chat_history")

    if message:  # 사용자가 메시지를 제공한 경우에만 처리
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("""
                Please answer in Korean
                You are an AI doctor counseling patients
                
                {chat_history}
            """),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        
        response = LLMChain(
            llm=llm, 
            prompt=prompt,
            verbose=True,
            memory=memorys[user]
        )
        
        # 언어 처리 모델로 메시지 처리 후 결과를 context에 추가
        context['llm_message'] = response.run(input=message)
        
        # ChatHistory 모델을 사용하여 대화 내용 저장
        ChatHistory.objects.create(
            chat_list_id_id=chat_list_id,
            username=str(user),
            message=message,
            div='user'
        )
        ChatHistory.objects.create(
            chat_list_id_id=chat_list_id,
            username='llm',
            message=context['llm_message'],
            div='llm'
        )

    return JsonResponse(context)

