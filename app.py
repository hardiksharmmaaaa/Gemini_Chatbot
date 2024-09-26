from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load the Gemini Pro Model to Get the Responses 

model=genai.GenerativeModel("gemini-pro")

chat=model.start_chat(history=[])  #this history will be stored 

def get_gemin_Response(question):
    response=chat.send_message(question,stream=True) #Stream=True means as LLm gives output, We will stream it 

    return response  #output 

#initialising the Streamlit app 

st.set_page_config(page_title="QNA Chatbot",page_icon="🦈")
st.header("Gemini Conversational QNA Chatbot")

# Initialzing the Session State for chat History If it doesnt exist (for storing the Chat History)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"]=[]  #storing the history 

input_text=st.text_input("Input:",key=input)

submit=st.button("Ask Your Question:")

if submit and input_text:
    response=get_gemin_Response(input_text)

    #Add the user query and response to the session Chat History 

    st.session_state["chat_history"].append(("you",input_text )) #storing all the conversation inside the you 

    st.subheader('The Response is :')

    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("bot",chunk.text)) #storing all the conversation inside the bot 
st.header("The Chat History is")

for role,text in st.session_state["chat_history"]:
    st.write(f"{role}:{text}")
