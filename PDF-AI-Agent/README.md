# PDF AI Agent

A Python-based PDF question-answering application that processes PDF documents and allows users to ask questions about their content from the terminal.

The project uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the PDF using semantic search and then uses **Google Gemini** to generate a context-based answer.

---

## Features

- Load PDF documents
- Extract text from PDF pages
- Split documents into smaller chunks
- Generate embeddings for document chunks
- Use HuggingFace Sentence Transformers for embeddings
- Store embeddings in FAISS vector database
- Search relevant content using semantic similarity
- Retrieve relevant PDF context
- Generate answers using Google Gemini
- Display source page numbers
- Interactive terminal-based question answering
- Environment variable support for API keys
- Prevent answers based on information outside the PDF context

---

## Technologies Used

- Python
- LangChain
- Google Gemini API
- HuggingFace Sentence Transformers
- FAISS
- PyPDF
- python-dotenv

### Embedding Model

```text
all-mpnet-base-v2
````

### Language Model

```text
Google Gemini
```

---

## RAG Architecture

```text
PDF Document
      |
      v
PDF Text Extraction
      |
      v
Text Chunking
      |
      v
HuggingFace Embeddings
      |
      v
FAISS Vector Database
      |
      |
User Question
      |
      v
Semantic Search
      |
      v
Relevant PDF Chunks
      |
      v
Google Gemini
      |
      v
Grounded Answer
      |
      v
Source Page Numbers
```

---

## Project Structure

```text
PDF-AI-Agent/
│
├── pdfs/
│   └── Placement Policy 2027_B.Tech_MCA.pdf
│
├── faiss_index/
│   └── FAISS vector database files
│
├── chat.py
├── ingest.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Installation

### 1. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies include:

```text
langchain
langchain-community
langchain-huggingface
langchain-text-splitters
sentence-transformers
faiss-cpu
pypdf
google-genai
python-dotenv
```

---

## Environment Configuration

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The Gemini API key is used for generating answers from the retrieved PDF context.

> Never commit your `.env` file or API key to GitHub.

---

## Usage

### Step 1: Add a PDF

Place the PDF document inside:

```text
pdfs/
```

Update the PDF path in `ingest.py` if necessary:

```python
PDF_PATH = "pdfs/Placement Policy 2027_B.Tech_MCA.pdf"
```

---

### Step 2: Create the FAISS Vector Database

Run:

```powershell
python ingest.py
```

The ingestion process:

1. Loads the PDF
2. Extracts the text
3. Splits the text into chunks
4. Generates HuggingFace embeddings
5. Creates the FAISS vector database
6. Saves the vector database locally

Example:

```text
======================================
       📄 PDF AI AGENT - INGEST
======================================

📖 Loading PDF: pdfs/Placement Policy 2027_B.Tech_MCA.pdf
✅ PDF loaded successfully
📄 Total pages: 4

✂️ Splitting PDF into chunks...
✅ Total chunks created: 19

🧠 Loading HuggingFace embeddings...
✅ Embedding model loaded

💾 Creating FAISS vector database...

======================================
       🎉 INGESTION COMPLETE
======================================
📄 Pages  : 4
🧩 Chunks : 19
🗄️ FAISS  : faiss_index
======================================
```

---

### Step 3: Start the AI Agent

Run:

```powershell
python chat.py
```

The application will load the FAISS vector database and start an interactive terminal session.

Example:

```text
======================================
       🚀 PDF AI AGENT READY
======================================

Ask questions about your PDF.
Type 'exit' to stop.

You: What are the placement eligibility criteria?
```

The system retrieves relevant sections from the PDF and provides them to Gemini as context.

---

## Example Questions

```text
What are the placement eligibility criteria?
```

```text
What are the placement eligibility criteria for B.Tech and MCA students?
```

```text
Is appearing in the pre-assessment test mandatory?
```

```text
How are students shortlisted for Dream companies?
```

```text
What role does IAMNEO play in placement preparation?
```

```text
Can students participate in campus placements after receiving an outside offer?
```

The agent also provides the relevant PDF page numbers used for the response.

---

## Grounded Question Answering

The AI agent is instructed to answer questions **only using the retrieved PDF context**.

If the requested information cannot be found in the retrieved content, the agent responds:

```text
I couldn't find this information in the PDF.
```

This helps reduce hallucinations and keeps answers grounded in the uploaded document.

---

## Example Output

```text
You: What are the placement eligibility criteria for B.Tech and MCA students?

🔎 Searching PDF...
🤔 Generating answer...

🤖 AI:

Based on the provided PDF context, specific academic eligibility
criteria are not detailed. However, the policy outlines general
eligibility conditions including participation willingness,
successful completion of the programme, and good conduct.

📚 Sources:
Page 1, Page 2, Page 3, Page 4
```

---

## How It Works

### 1. Document Ingestion

`ingest.py` loads the PDF using `PyPDFLoader`.

### 2. Text Chunking

The extracted content is divided into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

Current configuration:

```text
Chunk Size   : 500
Chunk Overlap: 50
```

### 3. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-mpnet-base-v2
```

from HuggingFace Sentence Transformers.

### 4. Vector Storage

The generated vectors are stored locally using:

```text
FAISS
```

### 5. Retrieval

When a user asks a question, FAISS performs semantic similarity search and retrieves the most relevant document chunks.

### 6. Answer Generation

The retrieved chunks are passed to Google Gemini along with the user's question.

Gemini generates an answer using the retrieved PDF context.

### 7. Source References

The application extracts page metadata from the retrieved documents and displays the relevant PDF pages.

---

## Files

### `ingest.py`

Responsible for:

* Loading the PDF
* Extracting document content
* Splitting text
* Generating embeddings
* Creating the FAISS database

### `chat.py`

Responsible for:

* Loading the FAISS database
* Retrieving relevant chunks
* Building the context
* Sending the context to Gemini
* Generating answers
* Displaying source pages

### `requirements.txt`

Contains the Python dependencies required to run the project.

### `.env`

Stores environment variables such as the Gemini API key.

---

## Future Improvements

* Web-based user interface
* PDF upload functionality
* Multiple PDF support
* Chat history
* Streaming responses
* Improved retrieval and ranking
* OCR support for scanned PDFs
* Metadata filtering
* Better source citations
* REST API
* Docker support
* Cloud deployment

---

## Purpose

This project was developed as a practical implementation of **RAG, semantic search, vector databases, and AI-powered document processing**.

It demonstrates how an AI application can retrieve relevant information from documents before generating an answer.

---

## Author

**Krishna Garg**# doc_q-a
