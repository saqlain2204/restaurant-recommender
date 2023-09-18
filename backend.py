from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext

from llama_index.llms import OpenAI
import openai

def indexing() -> None:
    """
    Parameters: None

    The function converts the data to whcih the LLM is grounded to vector indices and stores it in a json format in ./storage folder. The data from this folder is extracted in the main.py file

    Returns: None
    """
    st.secrets['key']
    docs = SimpleDirectoryReader('./data').load_data()
    # print(len(docs))
    service_context = ServiceContext.from_defaults(llm=OpenAI(temperature=0.8))
    index = VectorStoreIndex.from_documents(documents=docs, service_context=service_context)
    index.storage_context.persist()
    print("data stored in ./storage folder")

indexing()
