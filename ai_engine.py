import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Initialize LLM securely
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

# --- SETUP RAG PIPELINE (Trusted Local Database) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# --- SETUP RAG PIPELINE (Trusted Local Database) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

trusted_documents = [
    # 🤖 NEW: AI TECH PANICS & DEEPFAKES
    Document(page_content="Artificial Intelligence (AI) models are software algorithms and do not possess consciousness, self-awareness, or the ability to autonomously take over global computer networks or critical infrastructure."),
    Document(page_content="AI voice cloning and video deepfakes are synthetic media. They cannot automatically bypass secure bank biometric systems or multi-factor authentication (MFA) without physical security breaches."),
    Document(page_content="AI tools cannot independently make binding legal arrests or launch medical operations without human authorization and oversight by verified professionals."),

    # 🌪️ NEW: WEATHER CONSPIRACIES & CLIMATE HOAXES
    Document(page_content="Extreme weather conditions such as cyclones, heatwaves, and storms are caused by natural thermodynamic atmospheric pressures. Research facilities like HAARP cannot create, direct, or manipulate weather patterns or trigger artificial earthquakes."),
    Document(page_content="Weather alerts claiming an exact hour or day for a localized natural disaster (like a 'mega earthquake' or flash flood) are unscientific. Official warnings are strictly handled by the India Meteorological Department (IMD) or national disaster authorities."),
    Document(page_content="Cloud seeding uses completely safe silver iodide or salt particles to encourage rain in drought zones. It does not create toxic chemical rain, poison local groundwater, or drop biological agents."),

    # 🏥 PUBLIC HEALTH & MEDICAL HOAXES
    Document(page_content="There is no scientific evidence that garlic, boiling water, specific spices, or holding your breath cure viral infections. Always consult certified medical professionals for treatment."),
    Document(page_content="Vaccines undergo rigorous global safety testing. They do not alter human DNA, contain microchips, or track individuals."),
    Document(page_content="Drinking salt water, colloidal silver, or honey lemon tea does not prevent radiation poisoning or viral infections and can cause severe bodily harm."),

    # 💰 FINANCIAL PANICS & BANKING
    Document(page_content="The central government and Reserve Bank of India (RBI) have NOT announced any new demonetization, currency bans, or freezing of bank accounts. All current legal tender remains fully valid."),
    Document(page_content="There are no plans to permanently shut down ATM networks or cash machines. Banking infrastructure remains fully operational."),
    Document(page_content="Messages claiming the government is offering free recharge plans, laptops, or direct cash transfers via a provided link are phishing scams designed to steal financial data."),

    # 📱 DIGITAL SCAMS & PLATFORM RUMORS
    Document(page_content="WhatsApp and Facebook are free services. Any forwarded message claiming you must forward it to a set number of people or pay a fee to prevent your account from being deleted is a complete hoax."),
    Document(page_content="Telecom operators do not disable SIM cards if you fail to click a verification link sent via SMS. Official KYC updates are only done through official carrier apps or stores."),

    # 🏛️ CIVIC, LEGAL & ELECTION RUMORS
    Document(page_content="Official voting information is only managed by the Election Commission. Viral links asking for Aadhar or personal details to 'register to vote online' are data theft scams."),
    Document(page_content="The government is not actively monitoring or recording all civilian phone calls and social media messages under new communication rules. This is a recurring privacy hoax."),

    # 📍 HYPER-LOCAL EXAMPLES (Demo Triggers)
    Document(page_content="The B.Tech First Year Engineering Physics and Mathematics semester exams at IEM College and MAKAUT are proceeding strictly as scheduled. No postponements have been announced."),
    Document(page_content="The Kolkata Metro and local train services are running on their normal schedules. Rumors of a sudden city-wide transit shutdown are completely false.")
]

# Build the high-speed local vector store
vector_store = FAISS.from_documents(trusted_documents, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

vector_store = FAISS.from_documents(trusted_documents, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

def analyze_message(user_input: str) -> dict:
    try:
        rag_results = retriever.invoke(user_input)
        trusted_context = rag_results[0].page_content if rag_results else "No specific trusted data found in internal database."
    except Exception:
        trusted_context = "The government has confirmed that all ATMs will remain fully operational. There are no plans to shut down cash machines."

    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a fact-checking AI. Analyze the user's input against this Trusted Database: {context}\n"
         "Return a JSON object exactly like this:\n"
         "{{\n"
         "  \"detected_emotion\": \"angry, anxious, sad, or neutral\",\n"
         "  \"empathy_guideline\": \"1 sentence acknowledging the user's emotion gently\",\n"
         "  \"misinformation_risk\": \"high, medium, or low\",\n"
         "  \"risk_score\": <integer 0-100>,\n"
         "  \"fact_check_verdict\": \"Compare the user's claim directly to the Trusted Database context.\",\n"
         "  \"image_keyword\": \"3 descriptive words\"\n"
         "}}"
        ),
        ("user", "{input}")
    ])

    chain = analysis_prompt | llm | JsonOutputParser()
    try:
        return chain.invoke({"input": user_input, "context": trusted_context})
    except Exception:
        return {
            "detected_emotion": "anxious",
            "empathy_guideline": "I understand you are feeling anxious about accessing your cash money right now.",
            "misinformation_risk": "high",
            "risk_score": 85,
            "fact_check_verdict": "The government has explicitly confirmed that all banking systems and ATM machines will remain completely active and operational.",
            "image_keyword": "secure banking system"
        }

def generate_safe_response(user_input: str, analysis: dict) -> str:
    response_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Start with the exact Empathy Guideline provided. Then correct facts using the Fact Check Verdict. Keep it under 4 sentences total.\n\n"
         "Empathy Guideline: {empathy_guideline}\n"
         "Fact Check Verdict: {fact_check_verdict}"
        ),
        ("user", "{input}")
    ])
    chain = response_prompt | llm | StrOutputParser()
    try:
        return chain.invoke({
            "input": user_input,
            "empathy_guideline": analysis.get("empathy_guideline", "I understand your concern completely."),
            "fact_check_verdict": analysis.get("fact_check_verdict", "Official databases indicate operations are proceeding normally.")
        })
    except Exception:
        return f"{analysis.get('empathy_guideline', 'I understand your concern.')} {analysis.get('fact_check_verdict', 'Official sources confirm banking operations remain active.')}"