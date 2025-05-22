
# AI Prompt Engineering Microservice

## 🚀 Overview

A full-stack AI microservice that generates both **casual** and **formal** responses to user queries using Groq LLM, with:
- FastAPI backend (with PostgreSQL for history)
- Streamlit frontend
- User-specific prompt history
- Modular, tested codebase

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, psycopg2, Groq API
- **Frontend:** Streamlit
- **Database:** PostgreSQL (cloud-hosted, e.g., Render)
- **Testing:** unittest

---

## 📦 Project Structure

```
your-repo/
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── prompt_engineering.py   # Prompt logic (Groq API)
├── requirements.txt
├── .env.example
├── README.md
└── tests/
    ├── test_api.py
    ├── test_integration.py
    └── test_prompt_engineering.py
```

---

## 🤖 Prompt Strategies

- **Casual:**  
  `Explain this like you're talking to a friend: {query}`

- **Formal:**  
  `Write a formal and academic explanation of: {query}`

---

## 🏁 Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/SudoAnxu/prompt-engineering-ai-microservice
cd prompt-engineering-ai-microservice
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure environment variables

- Copy `.env.example` to `.env` and fill in your values:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
GROQ_API_KEY=your-groq-api-key
API_URL=https://your-backend.onrender.com
USER_ID=demo_user
FRONTEND_ORIGINS=https://your-streamlit-app.streamlit.app
```

### 4. Run the backend (FastAPI)

```
uvicorn main:app --reload
```

### 5. Run the frontend (Streamlit)

```
streamlit run app.py
```

---

## 🧪 Testing

Run all tests with:

```
python -m unittest discover -s tests
```

---

## 🌐 Hosted Demo

- **Frontend:** [streamlit-app.streamlit.app](https://prompt-engineering-ai-microservice-po9sjsxywyfiamhkbq5rzc.streamlit.app/)
- **Backend API docs:** [backend.onrender.com/docs](https://prompt-engineering-ai-microservice.onrender.com/docs)

---

## 📋 Features

- Generate casual and formal AI responses for any query
- Stores and displays user-specific prompt history
- Modular, well-documented code
- Unit and integration tests included

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

MIT 

---



