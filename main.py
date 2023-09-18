from llama_index import StorageContext, load_index_from_storage
import openai
import streamlit as st
from llama_index.memory import ChatMemoryBuffer

st.title("Restaurant Recommender Chatbot 👨‍🍳")

openai.api_key = st.secrets["key"]
index = None

@st.cache_resource
def fetch_index() -> index:
    """
    Paramater: None
    
    This function feteches the vector indices from the ./storage folder
    
    Returns: index -> vector indices are returned
    
    """
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
    
    return index

index = fetch_index()

# type(index) -> llama_index.indices.vector_store.base.VectorStoreIndex
# initialising the chat_engine with a `context` chatmode that takes into account the chat history while responding to user query.


memory = ChatMemoryBuffer.from_defaults(token_limit=25000)
chat_engine = index.as_chat_engine(
chat_mode="context",
memory = memory,
system_prompt=f"Assist in offering tailored hotel recommendations based on user inquiries, taking into account the desired location, budget constraints, and individual preferences. Ensure to present the most suitable options with comprehensive details regarding amenities, user reviews, and real-time availability. If you have access to URLs or web links associated with these recommendations, please provide them when available."
)


if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role" : "assistant",
            "content" : "Hey there! How can I help you? 👨‍🍳",
        }
    ]

if prompt:= st.chat_input("Enter your query"):
    st.session_state.messages.append(
        {
            "role" : "user",
            "content" : prompt,
        }
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# while(True):
#     user_query = str(input())
#     response = chat_engine.chat(user_query)
#     print(response)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Typing .."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {
                "role": "assistant", 
                "content": response.response
            }
            st.session_state.messages.append(message) 




