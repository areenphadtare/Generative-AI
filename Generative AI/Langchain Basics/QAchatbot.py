"Simple  Langchain Streamlit App with Groq"
from operator import index

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os



## Page Configuration
st.set_page_config(page_title="Simple Langchain Chatbot App with Groq")   


## Title the Groq Chat Model
st.title("Simple Langchain chat App with Groq")
st.markdown("This is a simple Langchain Streamlit app that uses Groq for chat functionality. You can ask questions and get responses from the AI model.") 



with st.sidebar:
    st.title("Langchain Chatbot App with Groq")
    st.markdown("This is a simple Langchain Streamlit app that uses Groq for chat functionality. You can ask questions and get responses from the AI model.") 
    st.markdown("## Instructions")
    st.markdown("1. Enter your question in the input box below.")
    st.markdown("2. Click the 'Ask' button to get a response from the AI model.")
    st.markdown("3. The response will be displayed below the input box.")   
## API Key Configuration
api_key=st.text_input("Enter your Groq API Key", type="password",help="You can get your Groq API key from https://groq.com/")   


##Model Selection
model_name = st.selectbox("Select a model", ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "openai/gpt-oss-safeguard-20b"], index=0, help="Select the model you want to use for chat functionality.")  

## Clear Button
if st.button("Clear Chat History"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared!") 

#initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = []

###initialize the LLM 
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        st.warning("Please enter your Groq API Key to use the chatbot.")
        return None
    # initialize the chat model
    llm = ChatGroq(groq_api_key=api_key, model=model_name, temperature=0.7, streaming=True)

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "{question}"),
        ]
    )

    # Create a chat chain
    chain = prompt | llm | StrOutputParser()
    return chain

# Get chain
chain = get_chain(api_key, model_name)
if not chain:
    st.warning("Please enter your Groq API Key to use the chatbot.")
    st.markdown("## Enter your question below and click 'Ask' to get a response from the AI model.")
else:
    # Get user input
    user_input = st.text_input("Enter your question:", key="user_input", help="Type your question here and press Enter or click 'Ask' to get a response from the AI model.")

    # Ask button
    if st.button("Ask"):
        if not user_input:
            st.warning("Please enter a question before clicking 'Ask'.")
        else:
            # Append user message to chat history
            st.session_state["chat_history"].append(HumanMessage(content=user_input))

            # Get response from the chain
            response = chain.run({"question": user_input})

            # Append AI message to chat history
            st.session_state["chat_history"].append(AIMessage(content=response))

            # Display chat history
            for message in st.session_state["chat_history"]:
                if isinstance(message, HumanMessage):
                    st.markdown(f"**You:** {message.content}")
                elif isinstance(message, AIMessage):
                    st.markdown(f"**AI:** {message.content}")

# Chat input
question = st.chat_input("Ask me Anything")
if question:
    st.session_state.messages.append(HumanMessage(content=question))
    with st.chat_message("user"):
        st.write(question)

    if chain:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                # Stream the response from the Groq model
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                # Add to the history
                st.session_state.messages.append(AIMessage(content=full_response))
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
     st.error("No chat model is available. Please enter your Groq API key.")
      
         