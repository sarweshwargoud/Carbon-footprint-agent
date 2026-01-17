from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def load_rag():
    loaders = [
        TextLoader("rag_docs/emission_factors.txt"),
        TextLoader("rag_docs/carbon_reduction.txt"),
        TextLoader("rag_docs/sustainability_standards.txt"),
        TextLoader("rag_docs/climate_policy.txt")
    ]

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="embeddings/chroma_db")
    vectordb.persist()

    return vectordb
