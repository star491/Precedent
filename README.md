# Precedent: Institutional Memory System

**Precedent** is an AI-powered engine that transforms unstructured meeting transcripts and documents into a structured "Institutional Memory". It allows organizations to search for the *reasoning* behind past decisions (e.g., "Why did we reject Azure?") rather than just keyword matches.

## 🚀 Features
*   **Reasoning Extraction:** Uses Groq (Llama-3) to extract detailed rationale, tradeoffs, and financial metrics.
*   **Semantic Search:** Vector-based retrieval (Qdrant) finds relevant decisions even without exact keyword matches.
*   **Privacy-First:** Embeddings are generated locally using `sentence-transformers`.
*   **Hybrid Filtering:** Filter by Team, Date, or Tags.

---

## 🛠️ Installation & Setup

### prerequisites
*   Python 3.10+
*   Node.js & npm

### 1. Clone the Repository
```bash
git clone https://github.com/SomyaPatidar06/Precedent.git
cd Precedent
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up Environment Variables
# Copy the example file to a real .env file
cp .env.example .env

# OPEN .env AND PASTE YOUR API KEY
# You need a free key from https://console.groq.com/keys
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

You need to run the Backend and Frontend in separate terminals.

**Terminal 1: Backend**
```bash
# Make sure you are in the root directory
python -m uvicorn backend.main:app --reload
```
*Backend runs on http://localhost:8000*

**Terminal 2: Frontend**
```bash
cd frontend
npm run dev
```
*Frontend runs on http://localhost:5173 (or similar)*

---

## 📖 Usage Guide
1.  **Ingest Data:** Go to the "Ingest" tab. Upload your meeting notes or PDFs.
2.  **Search:** Go to the "Search" tab. Ask natural questions like:
    *   *"Why did we choose Postgres over Mongo?"*
    *   *"What was the budget for the cloud migration?"*
3.  **View Context:** Click on a result to see the full Rationale, Alternatives, and Tradeoffs.

---

## 🏗️ Architecture
*   **Frontend:** React + Vite
*   **Backend:** FastAPI
*   **LLM:** Llama-3-70b (via Groq)
*   **Vector DB:** Qdrant (Embedded/Local)
*   **Embeddings:** all-MiniLM-L6-v2 (Local)
