import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Notice we removed the hardcoded key. The cloud server will inject it later securely.
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

# ... (the rest of your ai_engine.py code stays exactly the same)
# --- 1. SETUP RAG PIPELINE (Trusted Local Database) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

trusted_documents = [
    Document(page_content="The government has confirmed that all ATMs will remain fully operational. There are no plans to shut down cash machines."),
    Document(page_content="Boiling water does not cure viral infections. Viruses live inside the body's cells where hot water cannot reach them."),
    Document(page_content="Drinking salt water does not prevent radiation poisoning and can cause severe dehydration.")
]

vector_store = FAISS.from_documents(trusted_documents, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

def analyze_message(user_input: str) -> dict:
    rag_results = retriever.invoke(user_input)
    trusted_context = rag_results[0].page_content if rag_results else "No specific trusted data found in internal database."

    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a fact-checking AI. Analyze the user's input against this Trusted Database: {context}\n"
         "Return a JSON object exactly like this:\n"
         "{{\n"
         "  \"detected_emotion\": \"angry, anxious, sad, or neutral\",\n"
         "  \"empathy_guideline\": \"1 sentence on how to handle this emotional state\",\n"
         "  \"misinformation_risk\": \"high, medium, or low\",\n"
         "  \"risk_score\": <integer 0-100>,\n"
         "  \"fact_check_verdict\": \"Compare their claim to the Trusted Database context.\",\n"
         "  \"image_keyword\": \"A highly descriptive 3-word phrase\"\n"
         "}}"
        ),
        ("user", "{input}")
    ])

    chain = analysis_prompt | llm | JsonOutputParser()
    try:
        return chain.invoke({"input": user_input, "context": trusted_context})
    except Exception:
        return {
            "detected_emotion": "neutral",
            "empathy_guideline": "Provide standard guidance.",
            "misinformation_risk": "low",
            "risk_score": 10,
            "fact_check_verdict": "Analyzing internally.",
            "image_keyword": "abstract digital safety"
        }

def generate_safe_response(user_input: str, analysis: dict) -> str:
    response_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Start with the Empathy Guideline. Then correct facts using the Fact Check Verdict. Keep it under 4 sentences.\n\n"
         "Empathy Guideline: {empathy_guideline}\n"
         "Fact Check Verdict: {fact_check_verdict}"
        ),
        ("user", "{input}")
    ])
    chain = response_prompt | llm | StrOutputParser()
    try:
        return chain.invoke({
            "input": user_input,
            "empathy_guideline": analysis.get("empathy_guideline", "Please stay calm."),
            "fact_check_verdict": analysis.get("fact_check_verdict", "We are verifying this.")
        })
    except Exception as e:
        return "I understand this is a stressful topic. Let's look at the verified facts together."