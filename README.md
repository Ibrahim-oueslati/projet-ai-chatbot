## 📚 Ask Your Documents – AI Chatbot

> Upload your study materials (PDF or Word) and ask questions — an AI will find the answers for you using Groq + LangChain + ChromaDB.
<img width="1281" height="863" alt="image" src="https://github.com/user-attachments/assets/de6a1624-594f-4565-b597-0dad802a1c08" />


---

### 🚀 Features

* 📤 Upload PDF or DOCX files
* 🧠 AI processes documents and builds a knowledge base
* 💬 Ask natural questions about your content
* 🗂️ Keeps chat history for reference
* 🗑️ Manage uploaded documents
* 🤖 Powered by **Groq (LLaMA 3)**, **LangChain**, **ChromaDB**, and **HuggingFace Embeddings**

---

### 🛠️ Tech Stack

* [Streamlit](https://streamlit.io/) – Web app UI
* [LangChain](https://www.langchain.com/) – Retrieval-Augmented Generation (RAG)
* [Groq](https://groq.com/) – Ultra-fast inference with LLaMA 3
* [ChromaDB](https://www.trychroma.com/) – Local vector storage
* [HuggingFace Embeddings](https://huggingface.co/) – Text vectorization
* `.env` for API key management via [python-dotenv](https://github.com/theskumar/python-dotenv)

---

### 🧑‍💻 Local Installation

#### 1. **Clone the repo**

```bash
git clone https://github.com/Ibrahim-oueslati/projet-ai-chatbot.git
cd projet-ai-chatbot
```

#### 2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

#### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```
#### 4. **Add your Groq API key**

Create a `.env` file:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```
#### 5. **Run the app**

```bash
streamlit run app.py
```

---

### 📦 Folder Structure

```
projet-ai-chatbot/
│
├── app.py                # Main Streamlit app
├── .env                  # Secret key file (excluded)
├── .gitignore            # Git ignore rules
├── styles.css            # Custom UI styling (optional)
├── requirements.txt      # Python dependencies
└── uploaded_documents/   # Temporary uploaded documents
```

---

### 💡 Example Questions

Once your document is processed, try asking:

* "What is the summary of chapter 3?"
* "What does the term X mean?"
* "Explain the difference between X and Y"
* "List the steps for process Z"

---

### ⚠️ Disclaimer

This is an educational tool. Do **not** upload sensitive or private documents. Use at your own risk.

---

### 📄 License

MIT License © [Ibrahim Oueslati](https://github.com/Ibrahim-oueslati)

---

