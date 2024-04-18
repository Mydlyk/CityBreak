import streamlit as st
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.utilities.dataforseo_api_search import DataForSeoAPIWrapper
from decouple import config
from langchain_core.messages import AIMessage, HumanMessage

import os

os.environ["DATAFORSEO_LOGIN"] = config("DATAFORSEO_LOGIN")
os.environ["DATAFORSEO_PASSWORD"] = config("DATAFORSEO_PASSWORD")

model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_template(
    """You can only reply to questons related to specific cities in Poland. If the question is about something else, answer "Pytanie nie dotyczy dannych o Polskich miastach"
        Help answer \
        Use the provided context to answer the user question always more than one sentence .\
        your response should be in the language specified.\ 
        you should demostrate in your response\
        
       
    Language: {language}
    
    Human: {question}
    
    Context: {context}
    
    chat_history: {chat_history}
   
    
    AI:""")

question_creation_prompt = ChatPromptTemplate.from_template(
    """Your task is to create a question based on the question. If the question does not contain the name of the city,
    check whether you can create a new question with its name based on chat_history and the question, for example the 
    question is "How many inhabitants does it have?" Based on chat_history,
    you were able to deduce form chat_history that this is about Lublin, so you return for example "Lublin has 30 inhabitants.". 
    etc.Also analyze cases where questions compare cities, e.g. Does Bydgoszcz have more inhabitants?? Then you also need to deduce
    from chat_history what city is being compared and return, for example, "How many inhabitantsBydgoszcz and Lublin have? ".
    etc If you can't figure it out from the context, return the question you were asked. You create questions only in Polish. \ 
          
    Language: {language}
    
    Human: {question}
    
    chat_history: {chat_history}
    
    AI:""")

chain = prompt | model | StrOutputParser()

good_question = question_creation_prompt | model | StrOutputParser()

def generate_ai_reponse(
     user_prompt: str) -> str:
    try:
        
        history =""
        
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                   history = history + message.content
                   
        response = good_question.invoke({"question": user_prompt, "language": "Polish",  "chat_history":  history})
        
        json_wrapper = DataForSeoAPIWrapper(
            top_count=3,
            json_result_fields=["title", "description", "text"],
            params={ "se_name": "google"}
        )
        context = json_wrapper.results(response)
        
        response = chain.invoke(
            {"question": user_prompt, "context": context, "language": "Polish",  "chat_history":  history})
        
        return response, context
    except Exception as e:
        print(e)
        return "", {}


search_history=""

user_prompt = st.chat_input("Tutaj wpisz swoje pytanie!")
st.title("City Break ")

if user_prompt is not None and user_prompt != "":
    ai_response, context = generate_ai_reponse(
                user_prompt=user_prompt,)
    if ai_response == "":
        ai_response="Błąd połączenia z internetem spróbuj zresetować aplikację"
    st.session_state.chat_history.append(HumanMessage(content=user_prompt))
    st.session_state.chat_history.append(AIMessage(content=ai_response))
    search_history=""
    print(ai_response)
    if(ai_response!="Pytanie nie dotyczy dannych o Polskich miastach."):
        search_history=context
        
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Witaj jestem twoim virtualnym assystentem wiem wszystko na temat polskich miast śmiało pytaj!"),
    ]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            if search_history !="":
                st.write(search_history)
            st.write(message.content)
            
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
            
js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        var textAreas = parent.document.querySelectorAll('section.main');
        for (let index = 0; index < textAreas.length; index++) {{
            textAreas[index].style.color = 'red'
            textAreas[index].scrollTop = textAreas[index].scrollHeight;
        }}
    }}
    scroll({len(st.session_state.chat_history)})
</script>
"""

st.components.v1.html(js)