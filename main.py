from llama_index import StorageContext, load_index_from_storage
import openai
import streamlit as st


st.title("Restaurant Recommender Chatbot 👨‍🍳")

try:
    openai.api_key = st.secrets["key"]
except:
    st.write("Sorry the api key has expired. Please enter you own api key to continue")
    openai.api_key = st.text_area("Enter you key api key here")



index = None

if openai.api_key is not None:

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
    
    
    #initialising the chat_engine with a `context`` chatmode that takes into account the chat history while responding to user query.
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt="Assist in offering tailored hotel recommendations based on user inquiries, taking into account the desired location, budget constraints, and individual preferences. Ensure to present the most suitable options with comprehensive details regarding amenities, user reviews, and real-time availability. If you have access to URLs or web links associated with these recommendations, please provide them when available."
        )
    
    if 'messages' not in st.session_state.keys():
        st.session_state.messages = [
            {
                "role" : "Chef",
                "content" : "Hey there! How can I help you? 👨‍🍳"
    
            }
        ]

    if prompt:= st.chat_input("Enter your query"):
        st.session_state.messages.append(
            {
                "role" : "user",
                "content" : prompt
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
        with st.chat_message("Chef", avatar='👨‍🍳'):
            with st.spinner("Typing ..):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) 




