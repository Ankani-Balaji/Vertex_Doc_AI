# 📄 VertexDoc AI – Intelligent Document Assistant

## Overview

VertexDoc AI is an AI-powered document assistant built with **Flask, Gemini API, FAISS, and Sentence Transformers**. The application allows users to upload PDF documents, automatically extract their content, generate intelligent summaries, ask context-aware questions, and export AI conversations.

The project follows a clean service-based architecture and implements **Retrieval-Augmented Generation (RAG)** to provide accurate answers based only on the uploaded document.

---

# Features

### 📁 PDF Upload

* Upload PDF documents securely
* Validates file type before processing

### 📖 Text Extraction

* Extracts readable text using **PyPDF2**
* Displays a preview of the uploaded document

### 🤖 AI Document Summary

* Generates a structured summary using **Google Gemini**
* Highlights important information and key points

### 💡 AI Suggested Questions

* Automatically generates relevant questions based on document content
* One-click interaction for faster exploration

### 🔍 RAG-Based Document Chat

* Uses **FAISS Vector Store**
* Retrieves relevant document chunks
* Gemini answers strictly from retrieved context to reduce hallucinations

### 💬 Conversation History

* Maintains recent user interactions within the session
* Displays previous questions and answers

### 📄 Export Conversation

* Download conversation history as:

  * TXT
  * PDF

### ⚠ Error Handling

* Gracefully handles API failures and quota limits
* User-friendly flash messages
* Prevents application crashes

---

# Tech Stack

## Backend

* Python 3
* Flask

## AI & NLP

* Google Gemini API
* LangChain
* FAISS
* Sentence Transformers (all-MiniLM-L6-v2)

## PDF Processing

* PyPDF2

## Frontend

* HTML5
* Bootstrap 5
* CSS3
* JavaScript

## Export

* ReportLab

---

# Project Structure

```
vertex-doc-ai/

│── app.py
│── config.py
│── requirements.txt
│── README.md

├── routes/
│   ├── __init__.py
│   ├── upload.py
│   └── chat.py

├── services/
│   ├── __init__.py
│   ├── pdf_service.py
│   ├── rag_service.py
│   ├── summary_service.py
│   ├── question_service.py
│   ├── chat_service.py
│   └── export_service.py

├── templates/
│   ├── base.html
│   └── index.html

├── static/
│   ├── css/
│   └── js/

├── uploads/
└── vector_store/
```

---

# Installation

## 1. Clone the repository

```
git clone https://github.com/yourusername/vertex-doc-ai.git

cd vertex-doc-ai
```

## 2. Create a virtual environment

### Windows

```
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```
python3 -m venv venv

source venv/bin/activate
```

## 3. Install dependencies

```
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file:

```
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

SECRET_KEY=YOUR_SECRET_KEY
```

## 5. Run the application

```
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# How It Works

1. User uploads a PDF document.
2. PyPDF2 extracts readable text.
3. The text is divided into chunks.
4. Sentence Transformer converts chunks into embeddings.
5. FAISS stores vectors locally.
6. User asks a question.
7. FAISS retrieves the most relevant chunks.
8. Gemini receives only the retrieved context and generates an answer.
9. Conversation history can be exported as TXT or PDF.

---

# Retrieval-Augmented Generation (RAG)

Instead of sending the entire document to the language model, the application:

* Splits the document into chunks
* Generates vector embeddings
* Stores them in FAISS
* Retrieves only relevant chunks for each query

This approach improves:

* Accuracy
* Performance
* Context relevance
* Token efficiency

---

# Error Handling

The application includes:

* Invalid file validation
* Empty PDF detection
* Unsupported file handling
* Gemini API quota handling
* Friendly flash messages
* Graceful fallback responses

---

# Future Improvements

* OCR support for scanned PDFs
* Multi-document search
* Authentication system
* Persistent conversation storage
* Dark mode UI
* Document citations in answers
* Cloud deployment (Render/AWS)

---

# Author

**Ankani Balaji**

Python Developer | Flask | AI Applications | RAG | Web Development

---

# License

This project is developed for educational purposes and technical assessment demonstrations.
