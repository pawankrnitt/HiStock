# HiStock

HiStock is a financial research assistant built to analyze and answer complex questions about NVIDIA (NVDA) and Tesla (TSLA) stocks. It uses a LangGraph-powered ReAct agent to dynamically fetch real-time stock prices, recent news, and perform RAG (Retrieval-Augmented Generation) on ingested SEC filings and earnings transcripts.

## Features

- **Agentic Loop**: A full LangGraph state machine with Planning, Execution, Reflection, and Response nodes.
- **RAG Pipeline**: Ingests, chunks, and embeds financial documents (HTML/PDF) into Pinecone for lightning-fast semantic search.
- **Live Data**: Integrates with Alpha Vantage for live and historical stock prices, and NewsAPI for real-time news articles and analyst coverage.
- **Highly Grounded**: The LLM (Llama-3.3-70b-versatile via Groq) is strictly prompted to avoid hallucination, generating answers only from retrieved context and citing its sources inline.

## Tech Stack

- **Backend**: FastAPI, Python 3.10
- **AI / LLM**: LangChain, LangGraph, Groq (Llama 3.3 70B)
- **Vector Database**: Pinecone
- **Data APIs**: Alpha Vantage, NewsAPI

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/HiStock.git
cd HiStock/backend
```

### 2. Set up the virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the `backend/` directory using `.env.example` as a template. You will need API keys for:
- [Groq](https://console.groq.com/)
- [Pinecone](https://www.pinecone.io/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [NewsAPI](https://newsapi.org/)

```env
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=histock
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
NEWS_API_KEY=your_news_api_key
```

### 4. Run the Server
```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

Once the server is running, you can access the Swagger UI at `http://localhost:8000/docs`.

- `POST /api/v1/test/rag`: Tests the basic RAG pipeline (Phase 1).
- `POST /api/v1/test/agent`: Tests the full ReAct agentic loop with tool calling (Phase 2).

### Example Agent Query
**POST** `/api/v1/test/agent`
```json
{
  "question": "Why did NVDA spike in late 2024? Include price data and earnings context.",
  "company": "NVDA"
}
```
The agent will automatically plan to call `get_stock_price`, `search_news`, and `search_documents`, aggregate the context, reflect on its sufficiency, and return a cited response.
