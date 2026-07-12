import os
import chromadb
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from sentence_transformers import SentenceTransformer
import google.generativeai as genai


# load env file 
load_dotenv()


# chunking
def chunking(data , chunk_size = 500 , overlap=80):
    # splitter 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size ,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],      # smart cut (cut according to these chars)
        length_function=len
    )
    

    chunks = []
    chunks = splitter.split_text(data)


    return chunks  



# ---------------------------------------------------------------
#  ------ Embedding --------
api_key = os.getenv("API_KEY")
embedding_model = SentenceTransformer('intfloat/multilingual-e5-large')

def generate_embeddings(chunks):
    embeddings = embedding_model.encode(
        chunks,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings



# ---------------------------------------------------------------
#  ------ store embedded in vector DB --------



def store_in_vectorDB(chunks , embedded , collection_name = 'ard_zecola', persist_dir="./chroma_db"):
    # the interface between model and vector DB
    client = chromadb.PersistentClient(path=persist_dir)
    # collection which has vector content
    collection = client.get_or_create_collection(
        name = collection_name,
        metadata={"hnsw:space": "cosine"}       # cosign similarity
    )

    # ID for each chunk
    ids = [f'chunk{i}' for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embedded.tolist(),
        ids=ids
    )


    return collection



# ---------------------------------------------------------------
#  ------ Embedded Question --------

# get the fourth relevent vectors  
def query(question , collection , top_k=4):
    question_embedded  = embedding_model.encode([question] , convert_to_numpy=True)

    # get the result (most relevent)
    results = collection.query(
        query_embeddings=question_embedded.tolist(),
        n_results=top_k
    )



     # context from retrieved chunks
    context = "\n".join(results['documents'][0])
    
    # prompt for 
    prompt = f"""
    أنت مساعد ذكي متخصص في كتاب "أرض زيكولا" لعمرو عبد الحميد.
    استخدم المعلومات من السياق التالي للإجابة على السؤال باللغة العربية.
    إذا كانت الإجابة غير موجودة في النص، قل "لا أعرف" ولا تختلق إجابة.

    السياق:
    {context}

    السؤال: {question}
    
    الإجابة:
    """
    
    # gemini API
    genai.configure(api_key=api_key)
    # model = genai.GenerativeModel("gemini-1.5-flash-001")
    # model = genai.GenerativeModel("gemini-pro")
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    response = model.generate_content(" ايه هي رواية أرض زيكولا؟ ")
    print(response.text)

    response = model.generate_content(prompt)
    
    # return the answer and sources
    return {
        "answer": response.text,
        "sources": results['documents'][0],
        "source_ids": results['ids'][0]
    }