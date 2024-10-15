from langchain import hub
from langchain_upstage import UpstageEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableConfig
from langchain_community.llms import LlamaCpp
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict
from operator import itemgetter
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')


load_dotenv()

def format_docs(docs):
    return "\n\n".join(
        [
            f"<document><content>{doc.page_content}</content><source>{doc.metadata['source']}</source><page>{int(doc.metadata['page'])+1}</page></document>"
            for doc in docs
        ]
    )

file_path = ["YOUR_PDF_FILE_PATH"]
docs = []
for path in file_path:
    loader = PDFPlumberLoader(path)
    docs.extend(loader.load())
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=512, chunk_overlap=64
)
doc_splits = text_splitter.split_documents(docs)

embeddings_model = UpstageEmbeddings(model="solar-embedding-1-large")
vectorstore = FAISS.from_documents(documents=doc_splits, embedding=embeddings_model)

retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
llm = LlamaCpp(
    model_path="YOUR_LLM_PATH",
    n_ctx=2048,
    n_gpu_layers=-1,
    n_batch=512,
    temperature=0,
    verbose=False,
)

class GraphState(TypedDict):
    question: str
    context: str
    answer: str

def retrieve_document(state: GraphState) -> GraphState:
    print("---RETRIEVE---")
    retrieved_docs = retriever.invoke(state["question"])
    retrieved_docs = format_docs(retrieved_docs)
    return GraphState(context=retrieved_docs)

def llm_answer(state: GraphState) -> GraphState:
    print("---GENERATE---")
    question = state["question"]
    context = state["context"]

    prompt = hub.pull("teddynote/rag-korean-with-source")
    chain = {"question": itemgetter("question"), "context": itemgetter("context")} | prompt | llm | StrOutputParser()
    response = chain.invoke({"question": question, "context": context})

    return GraphState(answer=response)

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve_document)
workflow.add_node("llm_answer", llm_answer)

workflow.add_edge("retrieve", "llm_answer")

workflow.set_entry_point("retrieve")

memory = MemorySaver()

graph = workflow.compile(checkpointer=memory)

config = RunnableConfig(configurable={"thread_id": "RAG"})

inputs = GraphState(question="YOUR QUESTION")

for output in graph.stream(inputs, config=config):
    print(output)
