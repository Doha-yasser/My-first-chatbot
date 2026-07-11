# 📚 أرض زيكولا - Arabic RAG Chatbot

An end-to-end **Retrieval-Augmented Generation (RAG)** system built for the Arabic novel *"أرض زيكولا"* by Amr Abdelhamid. 
This project scrapes the book from a public Arabic library, handles scanned PDF pages using OCR, builds a persistent vector database, and serves an interactive Q&A chatbot via a Flask web interface.

## 🧠 How It Works (Pipeline)

1. **Web Scraping**: Fetches the PDF download URL from the Arabic library website using `BeautifulSoup`.
2. **PDF Download**: Downloads the book PDF and saves it locally.
3. **OCR Extraction**:
   - Converts scanned PDF pages to images using `pdf2image` (Poppler).
   - Extracts Arabic text using `pytesseract` (Tesseract OCR).
   - Cleans and saves the text as a `.txt` file (runs **only once**).
4. **Chunking**: Splits the long Arabic text into overlapping chunks using `LangChain`'s `RecursiveCharacterTextSplitter`.
5. **Embedding**: Generates dense vector embeddings for each chunk using the `intfloat/multilingual-e5-large` model (optimized for Arabic/multilingual tasks).
6. **Vector Storage**: Stores embeddings and text chunks in `ChromaDB` with Cosine similarity (runs **only once**).
7. **Retrieval & Generation**: 
   - User asks a question in Arabic.
   - The query is embedded and used to retrieve the top-k relevant chunks.
   - A custom prompt (with the retrieved context) is sent to **Google Gemini (Gemini-1.5-Flash)** to generate the final Arabic answer.
8. **User Interface**: Served via a `Flask` backend with a clean HTML frontend.

## 🛠️ Tech Stack

| Category | Technologies Used |
| :--- | :--- |
| **Web Scraping** | `requests`, `BeautifulSoup4` |
| **PDF/OCR** | `pdf2image`, `pytesseract`, `Poppler` |
| **Text Processing** | `LangChain Text Splitters` |
| **Embeddings** | `Sentence-Transformers` (`intfloat/multilingual-e5-large`) |
| **Vector DB** | `ChromaDB` |
| **LLM / Generation** | `Google Generative AI` (Gemini-1.5-Flash) |
| **Web Framework** | `Flask` |
| **Environment** | `python-dotenv` |

## 🚀 Getting Started

### Prerequisites

- **Python 3.12** or higher.
- **Tesseract OCR** installed on your system.
- **Poppler** installed on your system (required for `pdf2image`).

#### Windows Setup
1. Download and install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). 
   - Ensure you install the **Arabic language data** during setup.
2. Download [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) and extract the `bin` folder.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ard-zecola-rag.git
   cd ard-zecola-rag
