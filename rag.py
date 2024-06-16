# rag
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader

################################################
class ChatRAG:
    vector_store = None 
    retriever = None 
    chain = None

    def __init__(self, apikey:str):
        """
        Input:
            - apikey: str - chiave api openai
        """
        # definisco parametri del modello    
        self.model = ChatOpenAI(model = 'gpt-3.5-turbo', api_key=apikey)
        self.embedding = OpenAIEmbeddings(api_key = apikey)

        # costruizione del prompt
        self.template = """
        Usa il seguente contesto per rispondere alla domanda posta dall'utente.
        Se non conosci la risposta, puoi dire: Informazioni non trovate.
        Rispondi nella lingua della domanda.

        =================================
        {context}
        =================================

        Domanda: {question}

        Risposta:
        """
        self.prompt = PromptTemplate.from_template(self.template)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)

    def change_apikey(self, apikey_new:str):
        """
        Input
            - apikey_new: str - nuova chiave immessa dall'utente
        """
        self.model = ChatOpenAI(model = 'gpt-3.5-turbo', api_key=apikey_new)
        self.embedding = OpenAIEmbeddings(api_key = apikey_new)

    def ingest(self, link_user:str):
        """
        Input:
            - link_user: str - carichiamo il chromaDB
        """
        loader = WebBaseLoader(
            web_paths=[link_user]
        )
        docs = loader.load()

        if not docs:
            raise ValueError(f"Failed to load documents from {link_user}")

        docs_split = self.text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=docs_split, embedding=self.embedding)
        self.retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k":5,
                "score_threshold":0.5,
            },
        )

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                    | self.prompt
                    | self.model
                    | StrOutputParser())

    def ask(self, query: str):
        """
        Input: 
            - query: str - stringa della domanda posta dall'utente
        """
        if not self.chain:
            return "Please, insert a valid link."
        
        answer = self.chain.invoke(query)

        return answer
    
    def clear(self):
        """
        Ripuliamo il modello
        """
        self.vector_store = None
        self.retriever = None
        self.chain = None