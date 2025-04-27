

```markdown
# 🚀 FAST_API_BACKEND-CSAIL-

A FastAPI backend server designed to provide educational awareness on human trafficking for parents and children.  
It includes conversational AI capabilities, retrieval-augmented generation (RAG) for answering questions from curated PDFs, and fallback to GPT when needed.

---

## 📚 Features

- FastAPI-powered RESTful API
- Retrieval-Augmented Generation (RAG) chatbot using LangChain & ChromaDB
- Fallback to OpenAI (ChatGPT) if no relevant context is found
- SQLite database for session management and chat history storage
- Handles general greetings (hi, hello, thanks, bye) politely
- Clean JSON APIs for easy frontend integration
- Designed for Vercel serverless deployment
- Logging system (`app.log`) for request tracking

---

## 🚀 How to Run Locally

1. **Clone the Repository**

```bash
git clone https://github.com/direwolfsb/FAST_API_BACKEND-CSAIL-.git
cd FAST_API_BACKEND-CSAIL-
```

2. **Set up a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

3. **Install Requirements**

```bash
pip install -r requirements.txt
```

4. **Run the FastAPI Server**

```bash
uvicorn main:app --reload
```

✅ The server will start at:  
`http://127.0.0.1:8000`

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|:------|:---------|:------------|
| POST | `/chat` | Send a user question and get AI answer with optional sources |
| GET | `/get_history/{session_id}` | Retrieve full chat history and sources for a session |

---

## 🛠 Tech Stack

- **FastAPI** - Web framework
- **LangChain** - RAG pipeline
- **ChromaDB** - Vector database
- **OpenAI GPT** - Fallback model
- **SQLite** - Lightweight local database
- **Vercel** - Deployment platform (optional)

---

## ⚙️ Environment Variables

Before deploying or running production, set the following:

| Variable | Purpose |
|:--------|:--------|
| `OPENAI_API_KEY` | Your OpenAI API Key for GPT fallback |
| `DATABASE_URL` (optional) | If using external database |

---

## 🌐 Deployment

**Vercel (recommended)**

1. Add `vercel.json` and `api/index.py` (using Mangum)
2. Connect the GitHub repo to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy 🎯

---

## 📂 Project Structure

```
├── main.py         # FastAPI server
├── chroma_utils.py # ChromaDB utilities
├── db_utils.py     # SQLite database utilities
├── langchain_utils.py # LangChain RAG chain
├── pydantic_models.py # API request/response models
├── requirements.txt
├── app.log         # Log file
├── README.md
└── api/index.py    # (for Vercel deployment)
```

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome!  
Feel free to fork this repo and submit improvements 🚀

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ to help raise awareness about human trafficking.
```

---

# ✅ Ready!

You can copy-paste this into your project as `README.md`.

It will make your GitHub project look **professional and ready for portfolio/showcase**.  
✨

---

# 🚀 Bonus Tip
Would you like me to also generate a **`.gitignore`** and **`vercel.json`** file next?  
(so you can directly deploy this backend to Vercel after your push!)  
Just say **yes**! 🎯
