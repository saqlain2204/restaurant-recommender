from llama_index import StorageContext, load_index_from_storage
import openai
import streamlit as st

hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
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

chat_engine = index.as_chat_engine(
chat_mode="condense_question",
)

if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role" : "assistant",
            "content" : "Hey there! How can I help you? 👨‍🍳",
        }
    ]

if prompt:= st.chat_input("Enter your query"):
    import tiktoken

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    token_count = len(encoding.encode(prompt))
    print(f"The text contains {token_count} tokens.")
    st.session_state.messages.append(
        {
            "role" : "user",
            "content" : prompt,
        }
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        token_count = len(encoding.encode(message["content"]))
        print(f"The text contains {token_count} tokens.")

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




