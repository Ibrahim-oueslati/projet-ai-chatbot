import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # New import
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title=" Ask Your Documents", page_icon="📚", layout="wide")

if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📚 Ask Your Documents</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your study materials and ask questions - AI will find the answers!</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📤 Upload Your Files")
    uploaded_file = st.file_uploader("Choose a PDF or Word file", type=["pdf", "docx"])
    data_folder = "uploaded_documents"
    os.makedirs(data_folder, exist_ok=True)

    if uploaded_file:
        file_path = os.path.join(data_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.session_state.pop("documents_processed", None)

    files = [f for f in os.listdir(data_folder) if f.endswith(('.pdf', '.docx'))]
    st.markdown("### 📋 Your Uploaded Files:")
    if files:
        for f in files:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📄 {f}")
            with col2:
                if st.button("🗑️", key=f"delete_{f}"):
                    os.remove(os.path.join(data_folder, f))
                    st.success(f"🗑️ Deleted: {f}")
                    st.session_state.pop("documents_processed", None)
                    st.rerun()
    else:
        st.info("No files uploaded yet.")

with st.expander("🤔 How does this work?"):
    st.markdown("""
    1. **📤 Upload**: PDF or DOCX documents  
    2. **🔍 Process**: Text is split, embedded, and indexed  
    3. **💬 Ask**: Query and get smart answers!

    Great for students, researchers, or anyone studying from documents.
    """)

def init_ai():
    if "llm" not in st.session_state:
        if not GROQ_API_KEY:
            st.error("Please add your GROQ_API_KEY to the .env file")
            st.stop()
        st.session_state.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama3-8b-8192",
            temperature=0.1
        )

def process_documents():
    all_docs = []
    for file in files:
        path = os.path.join(data_folder, file)
        loader = PyPDFLoader(path) if file.endswith('.pdf') else Docx2txtLoader(path)
        all_docs.extend(loader.load())

    if not all_docs:
        st.warning("No readable content found.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedding=embeddings)

    st.session_state.qa_system = RetrievalQA.from_chain_type(
        llm=st.session_state.llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 3})
    )
    st.session_state.documents_processed = True
    st.success(f"✅ Processed {len(chunks)} text sections!")

if files:
    init_ai()
    if "documents_processed" not in st.session_state:
        with st.spinner("Processing your documents..."):
            process_documents()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.chat_history:
    st.markdown("### 💬 Conversation History")
    for msg in st.session_state.chat_history:
        role = "user-message" if msg["role"] == "user" else "bot-message"
        label = "🙋‍♂️ You asked:" if msg["role"] == "user" else "🤖 AI answered:"
        st.markdown(f"""<div class="{role}"><strong>{label}</strong> {msg["content"]}</div>""", unsafe_allow_html=True)

st.markdown("### 💭 Ask Your Question")
if not files:
    st.warning("⚠️ Please upload documents first.")
elif "documents_processed" not in st.session_state:
    st.info("📖 Processing in progress...")
else:
    with st.form("question_form", clear_on_submit=True):
        question = st.text_input("Ask something...", placeholder="E.g. What is chapter 3 about?")
        if st.form_submit_button("🚀 Get Answer") and question.strip():
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.qa_system.invoke({"query": question})
                    st.session_state.chat_history.append({"role": "assistant", "content": result["result"]})
                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"❌ Error: {str(e)}"
                    })
            st.rerun()

if st.session_state.get("documents_processed"):
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - What are the main points of the document?
        - What does [term] mean?
        - Explain [concept] simply.
        - How does X compare to Y?
        - What are the steps to do [process]?
        """)

if st.session_state.chat_history:
    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#666; padding:20px;">
    <h4>🎓 Perfect for Students and Researchers!</h4>
    <p>Built with ❤️ using Streamlit, LangChain & Groq</p>
</div>
""", unsafe_allow_html=True)
